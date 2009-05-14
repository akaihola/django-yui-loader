#!/usr/bin/python

__doc__ = r"""
    >>> from yui_loader.middleware import YUILoader, MODULE_INFO

    >>> n = YUILoader()
    >>> COMPONENTS = n._module_info

    >>> COMPONENTS['yahoo'].requires
    []

    >>> COMPONENTS['yahoo'].after
    ['sam', 'reset-fonts', 'grids', 'reset-fonts-grids', 'base', 'reset', 'fonts']

    >>> COMPONENTS['event'].requires
    ['yahoo']

    >>> COMPONENTS['yuiloader-dom-event'].after
    ['sam', 'reset-fonts', 'grids', 'reset-fonts-grids', 'base', 'reset', 'fonts']

    >>> sorted(COMPONENTS.get_rollups('event'))
    ['utilities', 'yahoo-dom-event', 'yuiloader-dom-event']

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

    >>> n.render()
    ''
    >>> list(n._sort_components())
    []
    >>> n.add_component('event') ; list(n._sort_components())
    ['yahoo', 'event']
    >>> print n.render()
    <script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/yahoo/yahoo-min.js"></script>
    <script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/event/event-min.js"></script>
    >>> n.add_component('dom') ; list(n._sort_components())
    ['yahoo-dom-event']
    >>> n.add_component('get') ; list(n._sort_components())
    ['yuiloader-dom-event']
    >>> n.add_component('yuiloader') ; list(n._sort_components())
    ['yuiloader-dom-event']
    >>> n.add_component('reset') ; list(n._sort_components())
    ['reset', 'yuiloader-dom-event']
    >>> n.add_component('base') ; list(n._sort_components())
    ['reset', 'base', 'yuiloader-dom-event']
    >>> n.add_component('fonts') ; list(n._sort_components())
    ['reset-fonts', 'base', 'yuiloader-dom-event']
    >>> n.add_component('grids') ; list(n._sort_components())
    ['reset-fonts-grids', 'base', 'yuiloader-dom-event']
    >>> print n.render()
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/reset-fonts-grids/reset-fonts-grids.css" />
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/base/base-min.css" />
    <script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/yuiloader-dom-event/yuiloader-dom-event.js"></script>
"""

if __name__ == '__main__':
    import sys, os, doctest
    from os.path import join, dirname
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    doctest.testmod()

