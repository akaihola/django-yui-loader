__doc__ = """
    >>> from django.conf import settings
    >>> settings.ROOT_URLCONF = 'yui_loader.tests.urls'

    >>> from django.test import Client
    >>> c = Client()
    >>> print c.get('/').content.replace(settings.YUI_INCLUDE_BASE, 'YUI_INCLUDE_BASE/')
    <html>
    <head>
    <title> test-yui-include.html </title>
    <link rel="stylesheet" type="text/css" href="YUI_INCLUDE_BASE/reset/reset-min.css" />
    <link rel="stylesheet" type="text/css" href="YUI_INCLUDE_BASE/fonts/fonts-min.css" />
    <link rel="stylesheet" type="text/css" href="YUI_INCLUDE_BASE/grids/grids-min.css" />
    <link rel="stylesheet" type="text/css" href="YUI_INCLUDE_BASE/base/base-min.css" />
    <script type="text/javascript" src="YUI_INCLUDE_BASE/yahoo/yahoo-debug.js"></script>
    <script type="text/javascript" src="YUI_INCLUDE_BASE/dom/dom-debug.js"></script>
    <script type="text/javascript" src="YUI_INCLUDE_BASE/selector/selector-debug.js"></script>
    <script type="text/javascript" src="YUI_INCLUDE_BASE/event/event-debug.js"></script>
    <script type="text/javascript" src="YUI_INCLUDE_BASE/element/element-debug.js"></script>
    <BLANKLINE>
    </head>
    <body>
    <BLANKLINE>
    <BLANKLINE>
    Haa! Haa!
    </body>
    </html>
    <BLANKLINE>

"""

if __name__ == '__main__':
    import sys, os, doctest
    from os.path import join, dirname
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'yui_loader.tests.settings'
    doctest.testmod()
