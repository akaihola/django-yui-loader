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
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/reset-fonts/reset-fonts.css" />
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/base/base-min.css" />
<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/yahoo-dom-event/yahoo-dom-event.js"></script>
<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/element/element-beta-min.js"></script>
<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/selector/selector-beta-min.js"></script>
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

import re
from django.conf import settings
from yui_loader.loader import YUILoader

PREFIX_RE = getattr(settings, 'YUI_INCLUDE_PREFIX_RE', '<!-- *YUI_')
SUFFIX_RE = getattr(settings, 'YUI_INCLUDE_SUFFIX_RE', ' *-->')

YUI_RE = re.compile(
    r'%s(include|version) +(.*?)%s' % (PREFIX_RE, SUFFIX_RE))
YUI_ADDMODULE_RE = re.compile(
    r'(?s)%saddModule\s*(\{\s*.*?\s*})\s*%s' % (PREFIX_RE, SUFFIX_RE))
YUI_INIT_RE = re.compile(
    '%sinit%s' % (PREFIX_RE, SUFFIX_RE))

ACCEPTED_CONTENT_TYPES = ('text/html',
                          'text/xml',
                          'application/xhtml+xml',
                          'application/xml')

class YUIIncludeMiddleware(object):
    def process_response(self, request, response):
        content_type = response['Content-Type'].split(';')[0]
        if content_type not in ACCEPTED_CONTENT_TYPES:
            return response
        components = set()
        loader = YUILoader()

        def add_module(match):
            loader.add_module(match.group(1))
            return ''
        content = YUI_ADDMODULE_RE.sub(add_module, response.content)

        def collect(match):
            cmd, data = match.groups()
            if cmd == 'include':
                components.update(data.split())
            elif cmd == 'version':
                loader.set_version(data)
            else:
                return '<!-- UNKNOWN COMMAND YUI_%s -->' % cmd
            return ''
        content = YUI_RE.sub(collect, content)

        for component in components:
            loader.add_component(component)

        tags = loader.render()
        if tags:
            content, count = YUI_INIT_RE.subn(tags, content, 1)
            if count != 1:
                content += ('<p>%d YUI init tags found,'
                            'at least one expected</p>' % count)
            response.content = YUI_INIT_RE.sub(
                '<!-- WARNING: MULTIPLE YUI init STATEMENTS -->', content)

        return response
