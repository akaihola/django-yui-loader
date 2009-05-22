#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import template
from django.template import Context
from django.template.loader import render_to_string

register = template.Library()

LOADER_URL = 'http://yui.yahooapis.com/2.7.0/build/' \
             'yuiloader/yuiloader-beta-min.js'


def indent(s, n):
    i = n * ' '
    return i + s.replace('\n', '\n' + i)

def join_indent(ls, n):
    return '\n'.join(indent(s, n) for s in ls)

def make_script_tag(script, src):
    if src:
        src_attrib = ' src="%s"' % src
    else:
        src_attrib = ''
    return '<script type="text/javascript"%s>%s</script>\n' % (
        src_attrib, script)


def script(script):
    return make_script_tag(script, None)


def script_src(src):
    return make_script_tag('', src)


def context_setdefault(context, varname, value):
    if varname not in context:
        context[varname] = value
    return context[varname]


@register.tag
def YUI(parser, token):
    bits = token.split_contents()[1:]
    if len(bits) < 1:
        raise template.TemplateSyntaxError, \
              'YUI requires at least the command name as an argument'
    cmd = bits.pop(0)

    if cmd == 'loader':
        if len(bits) > 2:
            raise template.TemplateSyntaxError, \
                  'YUI loader takes zero, one or two arguments'
        return YUILoaderNode(*bits)

    elif cmd == 'require':
        nodelists_add_module = []
        nodelist_on_success = parser.parse(('addModule', 'endYUI',))
        while True:
            token = parser.next_token()
            if token.contents == 'addModule':
                nodelists_add_module.append(
                    parser.parse(('addModule', 'endYUI',)))
            else:
                break
        return YUIRequireNode(bits, nodelist_on_success, nodelists_add_module)

    elif cmd == 'alias':
        aliases = [bit.split('=') for bit in bits]
        return YUIAliasNode((varname, module) for varname, module in aliases)
        # todo: tuple extraction error handling

    elif cmd == 'onDOMReady':
        if bits:
            raise template.TemplateSyntaxError, \
                  'YUI onDOMReady takes no arguments'
        nodelist = parser.parse(('endYUI',))
        parser.delete_first_token()
        return YUIOnDomReadyNode(nodelist)

    elif cmd == 'editor':
        if len(bits) != 1:
            raise template.TemplateSyntaxError, \
                  'YUI editor takes exactly one argument'
        return YUIEditorNode(bits[0])


def init(url):
    return ''.join((
        script_src(url),
        script('if (typeof(_DOMReady_funcs) == "undefined") {\n'
               '  _DOMReady_funcs = [];\n'
               '  function _onDOMReady(f) {\n'
               '    _DOMReady_funcs.push(f);\n'
               '  }\n'
               '}\n')))

ONDOMREADY = ('YAHOO.util.Event.onDOMReady(\n'
              '  function() {\n'
              '    for (var i=0;i<_DOMReady_funcs.length;++i)\n'
              '      _DOMReady_funcs[i]();\n'
              '    _onDOMReady = function(f) { f() };\n'
              '  }\n'
              ');\n')


class YUILoaderNode(template.Node):

    def __init__(self, url=None, filter=None):
        self.url = url and template.Variable(url)
        self.filter = filter and template.Variable(filter)

    def render(self, context):
        config = context_setdefault(context, '_yui', {})
        if self.filter is None:
            config['filter'] = None
        else:
            config['filter'] = self.filter.resolve(context)
        if self.url is None:
            config['source'] = LOADER_URL
        else:
            config['source'] = self.url.resolve(context)
        return YUIRequireNode(['dom', 'event']).render(context)


class YUIRequireNode(template.Node):

    def __init__(self, modules,
                 nodelist_on_success=None, nodelists_add_module=None):
        self.modules = modules
        self.nodelist_on_success = nodelist_on_success
        self.nodelists_add_module = nodelists_add_module or ()

    def render(self, context):
        result = []
        success_scripts = []
        config = context_setdefault(context, '_yui', {})

        if 'initialized' not in config:
            url = config.setdefault('source', LOADER_URL)
            result.append(init(url))
            success_scripts.append(ONDOMREADY)
            config['initialized'] = True
        result.append(script('_yui_loader = new YAHOO.util.YUILoader();'))

        if self.nodelist_on_success is not None:
            success_scripts.append(
                self.nodelist_on_success.render(context).strip())
        if success_scripts:
            on_success = \
              ',\n' \
              '  onSuccess: function() {\n' \
              '%s\n' \
              '}' % join_indent(success_scripts, 4)
        else:
            on_success = ''

        if config.get('filter', None):
            filtr = ',\n  filter: "%s"' % config['filter']
            if config['filter'].lower() == 'debug':
                filtr += ',\n  allowRollup: false'
        else:
            filtr = ''

        add_module = '\n'.join(
            '_yui_loader.addModule(%s);' % nodelist.render(context)
            for nodelist in self.nodelists_add_module)

        result.append(script(
            '%s\n'
            '_yui_loader.insert({\n'
            '  require: [%s]%s%s});' % (
            add_module,
            ', '.join('"%s"' % m for m in self.modules),
            filtr,
            on_success)))
        return ''.join(result)


class YUIAliasNode(template.Node):
    def __init__(self, aliases):
        self.aliases = aliases
    def render(self, context):
        assigned = context_setdefault(context, '_yui_assigned_aliases', set())
        assignments = [assignment for assignment in self.aliases
                       if assignment not in assigned]
        if not assignments:
            return ''
        assigned.update(assignments)
        return script('_onDOMReady(\n'
                      '  function() {\n'
                      '    %s\n'
                      '  }\n'
                      ');' %
                      ''.join('%s = %s;' % (varname, module)
                              for varname, module in assignments))
        #return script('YAHOO.util.Event.onDOMReady(function(){%s});' %
        #              ''.join('%s=%s;' % (varname, module)
        #                      for varname, module in assignments))


class YUIOnDomReadyNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context):
        #return script('YAHOO.util.Event.onDOMReady(%s);') % \
        #       self.nodelist.render(context)
        return script('_onDOMReady(%s);') % self.nodelist.render(context)


class YUIEditorNode(template.Node):
    def __init__(self, textarea_id):
        self.textarea_id = template.Variable(textarea_id)

    def render(self, context):
        textarea_id = self.textarea_id.resolve(context)
        return render_to_string(
            'yui/editor.html',
            {'yui_editor_textarea_id': textarea_id},
            Context())
