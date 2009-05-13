__doc__ = """
    >>> from django.test import Client
    >>> c = Client()
    >>> print c.get('/').content
    <html>
    <head>
    <title> test-yui-include.html </title>
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.5.1/build/reset/reset-min.css" />
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.5.1/build/fonts/fonts-min.css" />
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.5.1/build/grids/grids-min.css" />
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.5.1/build/base/base-min.css" />
    <script type="text/javascript" src="http://yui.yahooapis.com/2.5.1/build/yahoo/yahoo-debug.js"></script>
    <script type="text/javascript" src="http://yui.yahooapis.com/2.5.1/build/dom/dom-debug.js"></script>
    <script type="text/javascript" src="http://yui.yahooapis.com/2.5.1/build/selector/selector-beta-debug.js"></script>
    <script type="text/javascript" src="http://yui.yahooapis.com/2.5.1/build/event/event-debug.js"></script>
    <script type="text/javascript" src="http://yui.yahooapis.com/2.5.1/build/element/element-beta-debug.js"></script>
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
