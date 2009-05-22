import re
from shlex import shlex

from django.conf import settings

from yui_loader.module_info_2_7_0 import MODULE_INFO, SKIN
from yui_loader.components import Components


DEFAULT_BASE = 'http://yui.yahooapis.com/2.7.0/build/'
YUI_BASE = getattr(settings, 'YUI_INCLUDE_BASE', DEFAULT_BASE)

VERSIONS = {'raw': '', '': '', 'min': '-min', 'debug': '-debug'}

DEFAULT_JS_TAG = '<script type="text/javascript" src="%s"></script>'
DEFAULT_CSS_TAG = '<link rel="stylesheet" type="text/css" href="%s" />'
TAGS = {'js': getattr(settings, 'YUI_INCLUDE_JS_TAG', DEFAULT_JS_TAG),
        'css': getattr(settings, 'YUI_INCLUDE_CSS_TAG', DEFAULT_CSS_TAG)}

class YUILoader:

    def __init__(self, *components, **kwargs):
        self._module_info = Components(MODULE_INFO)
        self._components = set()
        self._rolled_up_components = {}
        self._rollup_counters = {}
        self.set_version(kwargs.pop('version', 'min'))
        for module in kwargs.pop('add_modules', ()):
            self.add_module(module)
        for component in components:
            self.add_component(component)

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

    def _urls_by_type(self, component_type):
        sorted_components = (self._module_info[component_name]
                             for component_name in self._sort_components())
        return [self._component_path(component)
                for component in sorted_components
                if component.type == component_type]

    def js_urls(self):
        return self._urls_by_type('js')

    def css_urls(self):
        return self._urls_by_type('css')

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

    def _component_path(self, component):
        path = component.fullpath or YUI_BASE + component.path
        if component.type == 'js':
            if self._version != '-min' and path.endswith('-min.js'):
                path = path[:-7] + self._version + '.js'
        elif component.type == 'css':
            if self._version == '' and path.endswith('-min.css'):
                path = path[:-8] + '.css'
        return path

    def _render_component(self, component_name):
        component = self._module_info[component_name]
        return TAGS[component.type] % self._component_path(component)

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
