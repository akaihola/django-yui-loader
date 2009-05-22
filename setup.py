__doc__ = """

YUI_include -- YUI Loader as Django middleware

(c) Antti Kaihola 2008,2009  http://djangopeople.net/akaihola/
                             akaihol+django@ambitone.com

This server-side middleware implements some of the functionality in the Yahoo
User Interface Loader component.  YUI JavaScript and CSS modules requirements
can be declared anywhere in the base, inherited or included templates, and the
resulting, optimized <script> and <link rel=stylesheet> tags are inserted at
the specified position of the resulting page.

Requirements may be specified in multiple locations.  This is useful when zero
or more components are included in the HTML head section, and inherited and/or
included templates require possibly overlapping sets of YUI components in the
body across inherited and included templates.  All tags are collected in the
head section, and duplicate tags are automatically eliminated.

The middleware understands component dependencies and ensures that resources
are loaded in the right order.  It knows about built-in rollup files that ship
with YUI.  By automatically using rolled-up files, the number of HTTP requests
is reduced.

The default syntax looks like HTML comments.  Markup for the insertion point is
replaced with <script> and <link> tags:
<!-- YUI_init -->

Component requirements are indicated, possibly in multiple locations, with the
``YUI_include`` markup.  It is removed from the resulting page by the
middleware. Example:
<!-- YUI_include fonts grids event dragdrop -->

Non-minified and compressed versions are requested, respectively, by:
<!-- YUI_version raw -->
<!-- YUI_version debug -->

Example:

<html><head>
<!-- YUI_init -->
<!-- YUI_include dom event -->
</head><body>
<!-- YUI_include element selector reset fonts base -->
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

The markup format can be customized with global Django settings.  Example:
YUI_INCLUDE_PREFIX_RE = r'{!'
YUI_INCLUDE_SUFFIX_RE = r'!}'
would change markup to e.g. ``{! init !}`` and ``{! include dom event !}``.

The base URL is customized with the ``YUI_INCLUDE_BASE`` setting, e.g.:
YUI_INCLUDE_BASE = 'http://localhost:8000/yui/build/'

To remove the XHTML trailing slash from the <link> tag, use:
YUI_INCLUDE_CSS_TAG = '<link rel="stylesheet" type="text/css" href="%s">'
"""

from setuptools import setup

setup(
    name='django-yui-loader',
    author='Antti Kaihola',
    author_email='akaihol+django@ambitone.com',
    maintainer='Antti Kaihola',
    maintainer_email='akaihol+django@ambitone.com',
    version='0.2',
    url='http://github.com/akaihola/django-yui-loader',
    py_modules=['yui_loader',
                'yui_loader.middleware',
                'yui_loader.module_info_2_5_1',
                'yui_loader.components',
                'yui_loader.context_processors'],
    description=('Server-side middleware which implements some of the '
                 'functionality in the Yahoo User Interface Loader '
                 'component.'),
    long_description=__doc__,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ]
)
