#!/usr/bin/python

__doc__ = r"""
    >>> import sys ; sys.setrecursionlimit(100)
    >>> from pprint import pprint
    >>> from django.conf import settings
    >>> from yui_loader.middleware import YUILoader

    >>> n = YUILoader()

    >>> n._module_info['yahoo'].requires
    []
    >>> n._module_info['yahoo'].after
    ['sam', 'reset-fonts', 'grids', 'reset-fonts-grids', 'base', 'reset', 'fonts']
    >>> n._module_info['event'].requires
    ['yahoo']
    >>> n._module_info['yuiloader-dom-event'].after
    ['sam', 'reset-fonts', 'grids', 'reset-fonts-grids', 'base', 'reset', 'fonts']
    >>> sorted(n._module_info.get_rollups('event'))
    ['utilities', 'yahoo-dom-event', 'yuiloader-dom-event']

    >>> pprint(n.add_module('''{
    ...     name: 'name', type: 'type', path: 'path', fullpath: 'fullpath',
    ...     requires: ['req1', 'req2'], after: ['after1', 'after2'],
    ...     optional: ['opt1', 'opt2'] }'''))
    {'after': ['after1', 'after2'],
     'fullpath': 'fullpath',
     'name': 'name',
     'optional': ['opt1', 'opt2'],
     'path': 'path',
     'requires': ['req1', 'req2'],
     'type': 'type'}

    >>> n.add_module('[')
    Traceback (most recent call last):
    ValueError: '{' expected instead of '['

    >>> n.add_module('{')
    Traceback (most recent call last):
    ValueError: 'name' or 'type' or 'path' or 'fullpath' or 'varName' or 'requires' or 'optional' or 'after' expected instead of end of data

    >>> n.add_module('{,')
    Traceback (most recent call last):
    ValueError: 'name' or 'type' or 'path' or 'fullpath' or 'varName' or 'requires' or 'optional' or 'after' expected instead of ','

    >>> n.add_module('{name')
    Traceback (most recent call last):
    ValueError: ':' expected instead of end of data

    >>> def test_sort(*c): return list(n._sort_components(set(c)))
    >>> test_sort('yahoo')
    ['yahoo']
    >>> test_sort('event')
    ['event']
    >>> test_sort('event', 'yahoo')
    ['yahoo', 'event']
    >>> test_sort('yahoo', 'event')
    ['yahoo', 'event']
    >>> test_sort('yahoo', 'event', 'dom', 'yuiloader')
    ['yahoo', 'dom', 'yuiloader', 'event']

    >>> def add(loader, component):
    ...     loader.add_component(component)
    ...     return list(loader._sort_components())

    >>> n.render()
    ''
    >>> list(n._sort_components())
    []
    >>> add(n, 'event')
    ['yahoo', 'event']
    >>> print n.render().replace(settings.YUI_INCLUDE_BASE, 'YUI_INCLUDE_BASE/')
    <script type="text/javascript" src="YUI_INCLUDE_BASE/yahoo/yahoo-min.js"></script>
    <script type="text/javascript" src="YUI_INCLUDE_BASE/event/event-min.js"></script>
    >>> add(n, 'dom')
    ['yahoo-dom-event']
    >>> add(n, 'get')
    ['yuiloader-dom-event']
    >>> add(n, 'yuiloader')
    ['yuiloader-dom-event']
    >>> add(n, 'reset')
    ['reset', 'yuiloader-dom-event']
    >>> add(n, 'base')
    ['reset', 'base', 'yuiloader-dom-event']
    >>> add(n, 'fonts')
    ['reset-fonts', 'base', 'yuiloader-dom-event']
    >>> add(n, 'grids')
    ['reset-fonts-grids', 'base', 'yuiloader-dom-event']

    >>> c = YUILoader()
    >>> add(c, 'reset-fonts')
    ['reset-fonts']
    >>> add(c, 'grids')
    ['reset-fonts-grids']

    >>> d = YUILoader()
    >>> add(d, 'grids')
    ['fonts', 'grids']
    >>> add(d, 'reset-fonts')
    ['reset-fonts-grids']

    >>> d.add_module("{name:'added',requires:['dom']}")
    Traceback (most recent call last):
    ValueError: type missing in "{name:'added',requires:['dom']}"

    >>> pprint(d.add_module("{type:'js',name:'added',requires:['dom']}"))
    {'name': 'added', 'requires': ['dom'], 'type': 'js'}

    >>> add(d, 'added')
    ['reset-fonts-grids', 'yahoo', 'dom', 'added']

The loader can be initialized in its constructor for easier direct
use:

    >>> e = YUILoader('charts')
    >>> list(e._sort_components())
    ['yahoo-dom-event', 'element', 'json', 'datasource', 'charts']

    >>> f = YUILoader('colorpicker', version='debug')
    >>> print f.render()
    <link rel="stylesheet" type="text/css" href="/js/yui/assets/skins/sam/skin.css" />
    <script type="text/javascript" src="/js/yui/yahoo/yahoo-debug.js"></script>
    <script type="text/javascript" src="/js/yui/slider/slider-debug.js"></script>
    <script type="text/javascript" src="/js/yui/element/element-debug.js"></script>
    <script type="text/javascript" src="/js/yui/colorpicker/colorpicker-debug.js"></script>
    <script type="text/javascript" src="/js/yui/dom/dom-debug.js"></script>
    <script type="text/javascript" src="/js/yui/event/event-debug.js"></script>
    <script type="text/javascript" src="/js/yui/dragdrop/dragdrop-debug.js"></script>

    >>> g = YUILoader('dummy', add_modules=(
    ...     "{type:'js',name:'dummy',requires:['fonts']}",))
    >>> list(g._sort_components())
    ['fonts', 'yahoo', 'dummy']

"""

if __name__ == '__main__':
    import sys, os, doctest
    from os.path import join, dirname
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'yui_loader.tests.settings'
    doctest.testmod()
