import re

from django.conf import settings

from module_info_2_5_1 import MODULE_INFO
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

COMPONENTS = Components(MODULE_INFO)


class YUILoader:

    def __init__(self):
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

    def render(self):
        return '\n'.join(self._render_component(component)
                         for component in self._sort_components())

    def _has_component(self, component_name):
        return component_name in self._components \
               or component_name in self._rolled_up_components

    def _get_satisfied_rollup(self, component_name):
        if self._version == '-min':
            for rollup_name in COMPONENTS.get_rollups(component_name):
                rollup_status = self._rollup_counters.get(rollup_name, set())
                if len(rollup_status) >= COMPONENTS[rollup_name].rollup:
                    return rollup_name

    def _count_in_rollups(self, component_name):
        for rollup_name in COMPONENTS.get_rollups(component_name):
            rolled_up = self._rollup_counters.setdefault(rollup_name, set())
            rolled_up.add(component_name)
        for superseded in COMPONENTS[component_name].supersedes:
            self._count_in_rollups(superseded)

    def _roll_up_superseded(self, component_name):
        for superseded in COMPONENTS[component_name].supersedes:
            self._rolled_up_components[superseded] = component_name
            if superseded in self._components:
                self._components.remove(superseded)

    def _add_requirements(self, component_name):
        for requirement in COMPONENTS[component_name].requires:
            self.add_component(requirement)

    def _render_component(self, component_name):
        component = COMPONENTS[component_name]
        path = component.path
        if component.type == 'js':
            if self._version != '-min' and path.endswith('-min.js'):
                path = path[:-7] + self._version + '.js'
        elif component.type == 'css':
            if self._version == '' and path.endswith('-min.css'):
                path = path[:-8] + '.css'
        return TAGS[component.type] % (YUI_BASE + path,)

    def _sort_components(self, component_names=None):
        if component_names is None:
            comps = self._components.copy()
        else:
            comps = component_names
        while comps:
            component_name = comps.pop()
            component = COMPONENTS[component_name]
            direct_deps = component.requires + component.after
            indirect_deps = [
                self._rolled_up_components[r] for r in direct_deps
                if r in self._rolled_up_components]
            all_deps = set(direct_deps).union(set(indirect_deps))
            deps_left = comps.intersection(all_deps)
            for r in self._sort_components(deps_left):
                yield r
                comps.remove(r)
            yield component_name


YUI_RE = re.compile(
    r'%s(include|version) +(.*?)%s' % (PREFIX_RE, SUFFIX_RE))
YUI_INIT_RE = re.compile(
    '%sinit%s' % (PREFIX_RE, SUFFIX_RE))

class YUIIncludeMiddleware(object):
    def process_response(self, request, response):
        components = set()
        node = YUILoader()
        def collect(match):
            cmd, data = match.groups()
            if cmd == 'include':
                components.update(data.split())
            elif cmd == 'version':
                node.set_version(data)
            else:
                return '<!-- UNKNOWN COMMAND YUI_%s -->' % cmd
            return ''
        content = YUI_RE.sub(collect, response.content)
        for component in components:
            node.add_component(component)
        content = YUI_INIT_RE.sub(node.render(), content, 1)
        response.content = YUI_INIT_RE.sub(
            '<!-- WARNING: MULTIPLE YUI_init STATEMENTS -->', content)
        return response
