
from django import template

register = template.Library()

DEFAULT_BASE = 'http://yui.yahooapis.com/2.5.1/build/'


class ComponentAdapter:

    def __init__(self, name, data):
        self.name = name
        self.data = data

    @property
    def supersedes(self):
        return self.data.get('supersedes', [])

    @property
    def requires(self):
        r = self.data.get('requires', [])

        if self.type != 'js' \
        or self.name == 'yahoo' \
        or 'yahoo' in self.supersedes \
        or 'yahoo' in r:
            return r
        else:
            return ['yahoo'] + r

    @property
    def after(self):
        if self.type == 'css':
            return self.data.get('after', [])
        elif self.type == 'js':
            return self.data.get('after', []) + COMPONENTS.get_css_components()

    @property
    def rollup(self):
        return self.data.get('rollup', 1)

    def __getattr__(self, attname):
        return self.data[attname]


class Components(dict):
    def __init__(self, components_dict):
        super(Components, self).__init__(components_dict)
        self.rollup_mapping = {}
        for component_name, data in components_dict.items():
            self.rollup_mapping.setdefault(component_name, set())
            if 'rollup' not in data:
                continue
            for rolled_up in data['supersedes']:
                self.rollup_mapping.setdefault(rolled_up, set()).add(
                    component_name)

    def __getitem__(self, component_name):
        data = super(Components, self).__getitem__(component_name)
        return ComponentAdapter(component_name, data)

    def get_rollups(self, component_name):
        return self.rollup_mapping[component_name]

    def get_css_components(self):
        return [name for name, data in self.items()
                if data['type'] == 'css']


COMPONENTS = Components({
    'animation': {'path': 'animation/animation-min.js',
                  'requires': ['dom', 'event'],
                  'type': 'js'},
    'autocomplete': {'optional': ['connection', 'animation'],
                     'path': 'autocomplete/autocomplete-min.js',
                     'requires': ['dom', 'event'],
                     'skinnable': True,
                     'type': 'js'},
    'base': {'after': ['reset', 'fonts', 'grids'],
             'path': 'base/base-min.css',
             'type': 'css'},
    'button': {'optional': ['menu'],
               'path': 'button/button-min.js',
               'requires': ['element'],
               'skinnable': True,
               'type': 'js'},
    'calendar': {'path': 'calendar/calendar-min.js',
                 'requires': ['event', 'dom'],
                 'skinnable': True,
                 'type': 'js'},
    'charts': {'path': 'charts/charts-experimental-min.js',
               'requires': ['element', 'json', 'datasource'],
               'type': 'js'},
    'colorpicker': {'optional': ['animation'],
                    'path': 'colorpicker/colorpicker-min.js',
                    'requires': ['slider', 'element'],
                    'skinnable': True,
                    'type': 'js'},
    'connection': {'path': 'connection/connection-min.js',
                   'requires': ['event'],
                   'type': 'js'},
    'container': {'optional': ['dragdrop', 'animation', 'connection'],
                  'path': 'container/container-min.js',
                  'requires': ['dom', 'event'],
                  'skinnable': True,
                  'supersedes': ['containercore'],
                  'type': 'js'},
    'containercore': {'path': 'container/container_core-min.js',
                      'pkg': 'container',
                      'requires': ['dom', 'event'],
                      'type': 'js'},
    'cookie': {'path': 'cookie/cookie-beta-min.js',
               'requires': ['yahoo'],
               'type': 'js'},
    'datasource': {'optional': ['connection'],
                   'path': 'datasource/datasource-beta-min.js',
                   'requires': ['event'],
                   'type': 'js'},
    'datatable': {'optional': ['calendar', 'dragdrop'],
                  'path': 'datatable/datatable-beta-min.js',
                  'requires': ['element', 'datasource'],
                  'skinnable': True,
                  'type': 'js'},
    'dom': {'path': 'dom/dom-min.js', 'requires': ['yahoo'], 'type': 'js'},
    'dragdrop': {'path': 'dragdrop/dragdrop-min.js',
                 'requires': ['dom', 'event'],
                 'type': 'js'},
    'editor': {'optional': ['animation', 'dragdrop'],
               'path': 'editor/editor-beta-min.js',
               'requires': ['menu', 'element', 'button'],
               'skinnable': True,
               'type': 'js'},
    'element': {'path': 'element/element-beta-min.js',
                'requires': ['dom', 'event'],
                'type': 'js'},
    'event': {'path': 'event/event-min.js',
              'requires': ['yahoo'],
              'type': 'js'},
    'fonts': {'path': 'fonts/fonts-min.css', 'type': 'css'},
    'get': {'path': 'get/get-min.js', 'requires': ['yahoo'], 'type': 'js'},
    'grids': {'optional': ['reset'],
              'path': 'grids/grids-min.css',
              'requires': ['fonts'],
              'type': 'css'},
    'history': {'path': 'history/history-min.js',
                'requires': ['event'],
                'type': 'js'},
    'imagecropper': {'path': 'imagecropper/imagecropper-beta-min.js',
                     'requires': ['dom',
                                  'event',
                                  'dragdrop',
                                  'element',
                                  'resize'],
                     'skinnable': True,
                     'type': 'js'},
    'imageloader': {'path': 'imageloader/imageloader-min.js',
                    'requires': ['event', 'dom'],
                    'type': 'js'},
    'json': {'path': 'json/json-min.js',
             'requires': ['yahoo'],
             'type': 'js'},
    'layout': {'optional': ['animation', 'dragdrop', 'resize', 'selector'],
               'path': 'layout/layout-beta-min.js',
               'requires': ['dom', 'event', 'element'],
               'skinnable': True,
               'type': 'js'},
    'logger': {'optional': ['dragdrop'],
               'path': 'logger/logger-min.js',
               'requires': ['event', 'dom'],
               'skinnable': True,
               'type': 'js'},
    'menu': {'path': 'menu/menu-min.js',
             'requires': ['containercore'],
             'skinnable': True,
             'type': 'js'},
    'profiler': {'path': 'profiler/profiler-beta-min.js',
                 'requires': ['yahoo'],
                 'type': 'js'},
    'profilerviewer': {'path': 'profilerviewer/profilerviewer-beta-min.js',
                       'requires': ['profiler', 'yuiloader', 'element'],
                       'skinnable': True,
                       'type': 'js'},
    'reset': {'path': 'reset/reset-min.css', 'type': 'css'},
    'reset-fonts': {'path': 'reset-fonts/reset-fonts.css',
                    'rollup': 2,
                    'supersedes': ['reset', 'fonts'],
                    'type': 'css'},
    'reset-fonts-grids': {'path': 'reset-fonts-grids/reset-fonts-grids.css',
                          'rollup': 4,
                          'supersedes': ['reset',
                                         'fonts',
                                         'grids',
                                         'reset-fonts'],
                          'type': 'css'},
    'resize': {'optional': ['animation'],
               'path': 'resize/resize-beta-min.js',
               'requires': ['dom', 'event', 'dragdrop', 'element'],
               'skinnable': True,
               'type': 'js'},
    'selector': {'path': 'selector/selector-beta-min.js',
                 'requires': ['yahoo', 'dom'],
                 'type': 'js'},
    'simpleeditor': {'optional': ['containercore',
                                  'menu',
                                  'button',
                                  'animation',
                                  'dragdrop'],
                     'path': 'editor/simpleeditor-beta-min.js',
                     'pkg': 'editor',
                     'requires': ['element'],
                     'skinnable': True,
                     'type': 'js'},
    'slider': {'optional': ['animation'],
               'path': 'slider/slider-min.js',
               'requires': ['dragdrop'],
               'type': 'js'},
    'tabview': {'optional': ['connection'],
                'path': 'tabview/tabview-min.js',
                'requires': ['element'],
                'skinnable': True,
                'type': 'js'},
    'treeview': {'path': 'treeview/treeview-min.js',
                 'requires': ['event'],
                 'skinnable': True,
                 'type': 'js'},
    'uploader': {'path': 'uploader/uploader-experimental.js',
                 'requires': ['yahoo'],
                 'type': 'js'},
    'utilities': {'path': 'utilities/utilities.js',
                  'rollup': 8,
                  'supersedes': ['yahoo',
                                 'event',
                                 'dragdrop',
                                 'animation',
                                 'dom',
                                 'connection',
                                 'element',
                                 'yahoo-dom-event',
                                 'get',
                                 'yuiloader',
                                 'yuiloader-dom-event'],
                  'type': 'js'},
    'yahoo': {'path': 'yahoo/yahoo-min.js', 'type': 'js'},
    'yahoo-dom-event': {'path': 'yahoo-dom-event/yahoo-dom-event.js',
                        'rollup': 3,
                        'supersedes': ['yahoo', 'event', 'dom'],
                        'type': 'js'},
    'yuiloader': {'path': 'yuiloader/yuiloader-beta-min.js',
                  'supersedes': ['yahoo', 'get'],
                  'type': 'js'},
    'yuiloader-dom-event': {'path': 'yuiloader-dom-event/yuiloader-dom-event.js',
                            'rollup': 5,
                            'supersedes': ['yahoo',
                                           'dom',
                                           'event',
                                           'get',
                                           'yuiloader',
                                           'yahoo-dom-event'],
                            'type': 'js'},
    'yuitest': {'path': 'yuitest/yuitest-min.js',
                'requires': ['logger'],
                'skinnable': True,
                'type': 'js'}}
)


@register.tag
def YUI_include(parser, token):
    '''
    Outputs <script> and <link rel="stylesheet"> tags for YAHOO User Interface
    library components.  This is essentially an implementation of the YUI
    Loader component as a Django template tag.

    {% YUI_include %} may be used multiple times, and all output appears at the
    first occurrence.  This is useful when zero or more components are included
    in the HTML head section, and inherited and/or included templates require
    possibly overlapping sets of YUI components in the body.  All tags are
    collected in the head section, and duplicate tags are automatically
    eliminated.

    {% YUI_include %} understands component dependencies and ensures that
    resources are loaded in the right order.  {% YUI_include %} knows about
    built-in rollup files that ship with YUI.  By automatically using rolled-up
    files, {% YUI_include %} reduces HTTP requests and keeps pages efficient.

    Example:

    <html><head>
    {% YUI_include dom event %}
    </head><body>
    {% YUI_include element selector reset fonts base %}
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
    '''
    bits = token.split_contents()[1:]
    initial_node, created = YUIIncludeNode.get_or_create(parser)
    for bit in bits:
        if bit.startswith('base='):
            if not created:
                raise template.TemplateSyntaxError, \
                      'YUI_include keyword options must be set ' \
                      'in the first occurrence of the tag'
            initial_node.set_base(bit[5:])
        elif bit in COMPONENTS:
            initial_node.add_component(bit)
        else:
            raise template.TemplateSyntaxError, \
                  'Unknown YUI component %r' % bit
    if created:
        return initial_node
    else:
        return template.TextNode('')


class YUIIncludeNode(template.Node):

    initial_nodes_by_parser = {}

    @classmethod
    def get_or_create(cls, parser):
        create = parser not in cls.initial_nodes_by_parser
        if create:
            cls.initial_nodes_by_parser[parser] = cls()
        return cls.initial_nodes_by_parser[parser], create

    def __init__(self):
        self._components = set()
        self._rolled_up_components = {}
        self._rollup_counters = {}
        self.set_base(DEFAULT_BASE)
        self.add_component('yahoo')

    def set_base(self, base):
        self._base = base

    def add_component(self, new_component_name):
        if not self._has_component(new_component_name):
            self._add_requirements(new_component_name)
            rollup_name = self._get_satisfied_rollup(new_component_name)
            if rollup_name:
                self.add_component(rollup_name)
            else:
                self._components.add(new_component_name)
                self._count_in_rollups(new_component_name)
                self._roll_up_superseded(new_component_name)

    def render(self, context):
        return '\n'.join(self._render_component(component)
                         for component in self._sort_components())

    def _has_component(self, component_name):
        return component_name in self._components \
               or component_name in self._rolled_up_components

    def _get_satisfied_rollup(self, new_component_name):
        for rollup_name in COMPONENTS.get_rollups(new_component_name):
            rollup_status = self._rollup_counters.get(rollup_name, set())
            if new_component_name not in rollup_status \
            and len(rollup_status)+1 >= COMPONENTS[rollup_name].rollup:
                return rollup_name

    def _count_in_rollups(self, new_component_name):
        for rollup_name in COMPONENTS.get_rollups(new_component_name):
            rolled_up = self._rollup_counters.setdefault(rollup_name, set())
            rolled_up.add(new_component_name)

    def _roll_up_superseded(self, new_component_name):
        for comp in COMPONENTS[new_component_name].supersedes:
            self._rolled_up_components[comp] = new_component_name
            if comp in self._components:
                self._components.remove(comp)

    def _add_requirements(self, new_component_name):
        for comp in COMPONENTS[new_component_name].requires:
            self.add_component(comp)

    def _render_component(self, component_name):
        component = COMPONENTS[component_name]
        if component.type == 'js':
            template = '<script type="text/javascript" src="%s"></script>'
        elif component.type == 'css':
            template = '<link rel="stylesheet" type="text/css" href="%s" />'
        else:
            return ''
        return template % (self._base + COMPONENTS[component_name].path,)

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
