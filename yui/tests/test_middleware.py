#!/usr/bin/python

__doc__ = r"""
    >>> import sys ; sys.setrecursionlimit(100)
    >>> from ambidjangolib.yui.middleware import \
    ...     COMPONENTS, YUILoader
    >>> COMPONENTS['yahoo'].requires
    []
    >>> COMPONENTS['yahoo'].after
    ['grids', 'reset-fonts', 'reset-fonts-grids', 'base', 'reset', 'fonts']
    >>> COMPONENTS['event'].requires
    ['yahoo']
    >>> COMPONENTS['yuiloader-dom-event'].after
    ['grids', 'reset-fonts', 'reset-fonts-grids', 'base', 'reset', 'fonts']
    >>> COMPONENTS.get_rollups('event')
    set(['utilities', 'yuiloader-dom-event', 'yahoo-dom-event'])

    >>> n = YUILoader()

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
"""

if __name__ == '__main__':
    from doctest import testmod
    testmod()
