#!/usr/bin/env python

__doc__ = r"""
Convert module information from an `yuiloader.js` file into a Python
module.  This script is used to generate the
`yui_loader/module_info_X_Y_Z.py` file.

Usage:

$ python convert_moduleinfo.py \
    <yui/build/yuiloader/yuiloader.js \
    >yui_loader/module_info_2_7_0.py
"""

import sys
import re
import json
import pprint

extract_skin = re.compile(r"'skin'\s*:\s*(\{.*?\})", re.S).search
extract_moduleinfo = re.compile(r"'moduleInfo'\s*:\s*(\{.*?\}\s*\})", re.S).search
is_comment = re.compile(r'\s*//').match

def encode_data(d, encoding='UTF-8'):
    if isinstance(d, unicode):
        return d.encode(encoding)
    elif isinstance(d, dict):
        return dict((key.encode(encoding), encode_data(value, encoding))
                    for key, value in d.iteritems())
    elif isinstance(d, list):
        return [encode_data(item) for item in d]
    else:
        return d

def fix_js(js):
    return ''.join(r for r in js.replace("'", '"').split('\n')
                   if not is_comment(r))

def extract(js, regexfunc):
    p = pprint.pformat(encode_data(json.loads(fix_js(regexfunc(js).group(1)))), indent=0)
    rows = p[1:-1].split('\n')
    return '{\n%s}' % '\n'.join('    %s' % r for r in rows)

def convert(stream):
    js = stream.read()
    moduleinfo = extract(js, extract_moduleinfo)
    skin = extract(js, extract_skin)
    print 'MODULE_INFO = %s\n' % moduleinfo
    print 'SKIN = %s\n' % skin
    print ("MODULE_INFO[SKIN['defaultSkin']] = {\n"
           "    'type': 'css',\n"
           "    'path': SKIN['base'] + SKIN['defaultSkin'] + '/' + SKIN['path'],\n"
           "    'after': SKIN['after'] }")

if __name__ == '__main__':
    convert(sys.stdin)
