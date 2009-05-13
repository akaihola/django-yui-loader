#!/usr/bin/python

__doc__ = r"""
    >>> import sys ; sys.setrecursionlimit(100)
    >>> from pprint import pprint
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
    >>> n._module_info.get_rollups('event')
    set(['utilities', 'yuiloader-dom-event', 'yahoo-dom-event'])

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
    >>> print n.render()
    <script type="text/javascript" src="http://yui.yahooapis.com/2.5.1/build/yahoo/yahoo-min.js"></script>
    <script type="text/javascript" src="http://yui.yahooapis.com/2.5.1/build/event/event-min.js"></script>
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

"""

if __name__ == '__main__':
    import sys, os, doctest
    from os.path import join, dirname
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'yui_loader.tests.settings'
    doctest.testmod()
