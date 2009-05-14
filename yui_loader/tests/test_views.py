__doc__ = """
    >>> from django.test import Client
    >>> c = Client()
    >>> print c.get('/').content
    <html>
    <head>
    <title> test-yui-include.html </title>
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/reset/reset-min.css" />
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/fonts/fonts-min.css" />
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/grids/grids-min.css" />
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/base/base-min.css" />
    <script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/yahoo/yahoo-debug.js"></script>
    <script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/dom/dom-debug.js"></script>
    <script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/selector/selector-debug.js"></script>
    <script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/event/event-debug.js"></script>
    <script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/element/element-debug.js"></script>
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
