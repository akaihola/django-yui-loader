#!/usr/bin/python

__doc__ = r"""
    >>> from ambidjangolib.yui.templatetags.yui_include import \
    ...     COMPONENTS, YUIIncludeNode
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

    >>> n = YUIIncludeNode()

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

    >>> n.render(None)
    '<script type="text/javascript" src="http://yui.yahooapis.com/2.5.1/build/yahoo/yahoo-min.js"></script>'
    >>> list(n._sort_components())
    ['yahoo']
    >>> n.add_component('event') ; list(n._sort_components())
    ['yahoo', 'event']
    >>> n.add_component('dom') ; list(n._sort_components())
    ['yahoo-dom-event']
    >>> n.add_component('get') ; list(n._sort_components())
    ['yahoo-dom-event', 'get']
    >>> n.add_component('yuiloader') ; list(n._sort_components())
    ['yuiloader-dom-event']
    >>> n.add_component('reset') ; list(n._sort_components())
    ['reset', 'yuiloader-dom-event']
    >>> n.add_component('base') ; list(n._sort_components())
    ['reset', 'base', 'yuiloader-dom-event']
    >>> n.add_component('fonts') ; list(n._sort_components())
    ['reset-fonts', 'base', 'yuiloader-dom-event']
    >>> n.add_component('grids') ; list(n._sort_components())
    ['reset-fonts', 'grids', 'base', 'yuiloader-dom-event']
"""

if __name__ == '__main__':
    from doctest import testmod
    testmod()
