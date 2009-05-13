__doc__ = """

YUI_include -- YUI Loader as Django middleware

(c) Antti Kaihola 2008  http://djangopeople.net/akaihola/
                        akaihol+django@ambitone.com

This server-side middleware implements some of the functionality in the Yahoo
User Interface Loader component.  YUI JavaScript and CSS modules requirements
can be declared anywhere in the base, inherited or included templates, and the
resulting, optimized <script> and <link rel=stylesheet> tags are inserted at
the specified position of the resulting page.

Requirements may be specified in multiple locations.  This is useful when zero
or more components are included in the HTML head section, and inherited and/or
included templates require possibly overlapping sets of YUI components in the
body across inherited and included templates.  All tags are collected in the
head section, and duplicate tags are automatically eliminated.

The middleware understands component dependencies and ensures that resources
are loaded in the right order.  It knows about built-in rollup files that ship
with YUI.  By automatically using rolled-up files, the number of HTTP requests
is reduced.

The default syntax looks like HTML comments.  Markup for the insertion point is
replaced with <script> and <link> tags:
<!-- YUI_init -->

Component requirements are indicated, possibly in multiple locations, with the
``YUI_include`` markup.  It is removed from the resulting page by the
middleware. Example:
<!-- YUI_include fonts grids event dragdrop -->

Non-minified and compressed versions are requested, respectively, by:
<!-- YUI_version raw -->
<!-- YUI_version debug -->

Example:

<html><head>
<!-- YUI_init -->
<!-- YUI_include dom event -->
</head><body>
<!-- YUI_include element selector reset fonts base -->
</body></html>

Renders:

<html><head>
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.5.1/build/reset-fonts/reset-fonts.css" />
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.5.1/build/base/base-min.css" />
<script type="text/javascript" src="http://yui.yahooapis.com/2.5.1/build/yahoo-dom-event/yahoo-dom-event.js"></script>
<script type="text/javascript" src="http://yui.yahooapis.com/2.5.1/build/element/element-beta-min.js"></script>
<script type="text/javascript" src="http://yui.yahooapis.com/2.5.1/build/selector/selector-beta-min.js"></script>
</head><body>
</body></html>

The markup format can be customized with global Django settings.  Example:
YUI_INCLUDE_PREFIX_RE = r'{!'
YUI_INCLUDE_SUFFIX_RE = r'!}'
would change markup to e.g. ``{! init !}`` and ``{! include dom event !}``.

The base URL is customized with the ``YUI_INCLUDE_BASE`` setting, e.g.:
YUI_INCLUDE_BASE = 'http://localhost:8000/yui/build/'

To remove the XHTML trailing slash from the <link> tag, use:
YUI_INCLUDE_CSS_TAG = '<link rel="stylesheet" type="text/css" href="%s">'
"""

import re
from shlex import shlex

from django.conf import settings

from module_info_2_5_1 import MODULE_INFO, SKIN
from components import Components


DEFAULT_BASE = 'http://yui.yahooapis.com/2.5.1/build/'
DEFAULT_JS_TAG = '<script type="text/javascript" src="%s"></script>'
DEFAULT_CSS_TAG = '<link rel="stylesheet" type="text/css" href="%s" />'

YUI_BASE = getattr(settings, 'YUI_INCLUDE_BASE', DEFAULT_BASE)
PREFIX_RE = getattr(settings, 'YUI_INCLUDE_PREFIX_RE', '<!-- *YUI_')
SUFFIX_RE = getattr(settings, 'YUI_INCLUDE_SUFFIX_RE', ' *-->')
TAGS = {'js': getattr(settings, 'YUI_INCLUDE_JS_TAG', DEFAULT_JS_TAG),
        'css': getattr(settings, 'YUI_INCLUDE_CSS_TAG', DEFAULT_CSS_TAG)}
VERSIONS = {'raw': '', '': '', 'min': '-min', 'debug': '-debug'}


class YUILoader:

    def __init__(self):
        self._module_info = Components(MODULE_INFO)
        self._components = set()
        self._rolled_up_components = {}
        self._rollup_counters = {}
        self.set_version('min')

    def set_version(self, version):
        self._version = VERSIONS[version]

    def add_component(self, new_component_name):
        if not self._has_component(new_component_name):
            self._add_requirements(new_component_name)
            self._count_in_rollups(new_component_name)
            rollup_name = self._get_satisfied_rollup(new_component_name)
            if rollup_name:
                self.add_component(rollup_name)
            else:
                self._components.add(new_component_name)
                self._roll_up_superseded(new_component_name)

    def add_module(self, module_def):
        module_data = {}
        lexer = shlex(module_def, posix=True)

        def expect(*patterns):
            token = lexer.get_token()
            if token not in patterns:
                raise ValueError, '%s expected instead of %s' % \
                      (' or '.join(repr(s) for s in patterns),
                       token and repr(token) or 'end of data')
            return token

        str_attrs = 'name', 'type', 'path', 'fullpath', 'varName'
        list_attrs = 'requires', 'optional', 'after'
        state = 'ATTR'
        expect('{')
        while state != 'STOP':
            if state == 'ATTR':
                token = expect(*str_attrs+list_attrs)
                expect(':')
                if token in str_attrs:
                    module_data[token] = lexer.get_token()
                    if module_data[token] is None:
                        raise ValueError, \
                              'string expected instead of end of data'
                    state = 'DELIM'
                elif token in list_attrs:
                    expect('[')
                    lst = module_data[token] = []
                    state = 'LIST'
            elif state == 'LIST':
                lst.append(lexer.get_token())
                if re.search(r'\W', lst[-1]):
                    raise ValueError, 'invalid component name %r' % token
                if expect(',', ']') == ']':
                    state = 'DELIM'
            elif state == 'DELIM':
                if expect(',', '}') == '}':
                    expect(None)
                    state = 'STOP'
                else:
                    state = 'ATTR'

        if 'type' not in module_data:
            raise ValueError, 'type missing in %r' % module_def
        self._module_info.add(module_data['name'], module_data)
        return module_data

    def render(self):
        return '\n'.join(self._render_component(component)
                         for component in self._sort_components())

    def _has_component(self, component_name):
        return component_name in self._components \
               or component_name in self._rolled_up_components

    def _get_satisfied_rollup(self, component_name):
        if self._version == '-min':
            for rollup_name in self._module_info.get_rollups(component_name):
                rollup_status = self._rollup_counters.get(rollup_name, set())
                if len(rollup_status) >= self._module_info[rollup_name].rollup:
                    return rollup_name

    def _count_in_rollups(self, component_name):
        for rollup_name in self._module_info.get_rollups(component_name):
            rolled_up = self._rollup_counters.setdefault(rollup_name, set())
            rolled_up.add(component_name)
        for superseded in self._module_info[component_name].supersedes:
            self._count_in_rollups(superseded)

    def _roll_up_superseded(self, component_name):
        for superseded in self._module_info[component_name].supersedes:
            self._rolled_up_components[superseded] = component_name
            if superseded in self._components:
                self._components.remove(superseded)

    def _add_requirements(self, component_name):
        component = self._module_info[component_name]
        for requirement in component.requires:
            self.add_component(requirement)
        if component.skinnable:
            self.add_component(SKIN['defaultSkin'])

    def _render_component(self, component_name):
        component = self._module_info[component_name]
        path = component.fullpath or YUI_BASE + component.path
        if component.type == 'js':
            if self._version != '-min' and path.endswith('-min.js'):
                path = path[:-7] + self._version + '.js'
        elif component.type == 'css':
            if self._version == '' and path.endswith('-min.css'):
                path = path[:-8] + '.css'
        return TAGS[component.type] % path

    def _sort_components(self, component_names=None):
        if component_names is None:
            comps = self._components.copy()
        else:
            comps = component_names
        while comps:
            component_name = comps.pop()
            component = self._module_info[component_name]
            direct_deps = component.requires + component.after
            indirect_deps = [
                self._rolled_up_components[r] for r in direct_deps
                if r in self._rolled_up_components]
            all_deps = set(direct_deps) \
                       .union(set(indirect_deps)) \
                       .union(set(component.optional))
            deps_left = comps.intersection(all_deps)
            for r in self._sort_components(deps_left):
                yield r
                comps.remove(r)
            yield component_name


YUI_RE = re.compile(
    r'%s(include|version) +(.*?)%s' % (PREFIX_RE, SUFFIX_RE))
YUI_ADDMODULE_RE = re.compile(
    r'(?s)%saddModule\s*(\{\s*.*?\s*})\s*%s' % (PREFIX_RE, SUFFIX_RE))
YUI_INIT_RE = re.compile(
    '%sinit%s' % (PREFIX_RE, SUFFIX_RE))

class YUIIncludeMiddleware(object):
    def process_response(self, request, response):
        components = set()
        loader = YUILoader()

        def add_module(match):
            loader.add_module(match.group(1))
            return ''
        content = YUI_ADDMODULE_RE.sub(add_module, response.content)

        def collect(match):
            cmd, data = match.groups()
            if cmd == 'include':
                components.update(data.split())
            elif cmd == 'version':
                loader.set_version(data)
            else:
                return '<!-- UNKNOWN COMMAND YUI_%s -->' % cmd
            return ''
        content = YUI_RE.sub(collect, content)

        for component in components:
            loader.add_component(component)

        tags = loader.render()
        if tags:
            content, count = YUI_INIT_RE.subn(tags, content, 1)
            if count != 1:
                content += ('<p>%d YUI init tags found,'
                            'at least one expected</p>' % count)
            response.content = YUI_INIT_RE.sub(
                '<!-- WARNING: MULTIPLE YUI init STATEMENTS -->', content)

        return response
