================================================
 YUI_include -- YUI Loader as Django middleware
================================================

:Copyright: 2008-2009, Antti Kaihola and individual contributors
:Contact:   akaihol+django@ambitone.com
:License:   BSD, see the file LICENSE for details

Description
===========

This server-side middleware implements some of the functionality in
the Yahoo User Interface Loader component.  YUI JavaScript and CSS
modules requirements can be declared anywhere in the base, inherited
or included templates, and the resulting, optimized ``<script>`` and
``<link rel=stylesheet>`` tags are inserted at the specified position
of the resulting page.

Requirements may be specified in multiple locations.  This is useful
when zero or more components are included in the HTML head section,
and inherited and/or included templates require possibly overlapping
sets of YUI components in the body across inherited and included
templates.  All tags are collected in the head section, and duplicate
tags are automatically eliminated.

The middleware understands component dependencies and ensures that
resources are loaded in the right order.  It knows about built-in
rollup files that ship with YUI.  By automatically using rolled-up
files, the number of HTTP requests is reduced.

Syntax
======

The default syntax looks like HTML comments.  Markup for the insertion
point is replaced with ``<script>`` and ``<link>`` tags::

    <!-- YUI_init -->

Component requirements are indicated, possibly in multiple locations,
with the ``YUI_include`` markup.  It is removed from the resulting
page by the middleware. Example::

    <!-- YUI_include fonts grids event dragdrop -->

Non-minified and compressed versions are requested, respectively, by::

    <!-- YUI_version raw -->
    <!-- YUI_version debug -->

Example
=======

::

    <html><head>
    <!-- YUI_init -->
    <!-- YUI_include dom event -->
    </head><body>
    <!-- YUI_include element selector reset fonts base -->
    </body></html>

The above HTML will render as::

    <html><head>
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.5.1/build/reset-fonts/reset-fonts.css" />
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.5.1/build/base/base-min.css" />
    <script type="text/javascript" src="http://yui.yahooapis.com/2.5.1/build/yahoo-dom-event/yahoo-dom-event.js"></script>
    <script type="text/javascript" src="http://yui.yahooapis.com/2.5.1/build/element/element-beta-min.js"></script>
    <script type="text/javascript" src="http://yui.yahooapis.com/2.5.1/build/selector/selector-beta-min.js"></script>
    </head><body>
    </body></html>

Customization
=============

The markup format can be customized with global Django settings.
Example::

    YUI_INCLUDE_PREFIX_RE = r'{!'
    YUI_INCLUDE_SUFFIX_RE = r'!}'

would change markup to e.g. ``{! init !}`` and ``{! include dom event !}``.

The base URL is customized with the ``YUI_INCLUDE_BASE`` setting,
e.g.::

    YUI_INCLUDE_BASE = 'http://localhost:8000/yui/build/'

To remove the XHTML trailing slash from the ``<link>`` tag, use::

    YUI_INCLUDE_CSS_TAG = '<link rel="stylesheet" type="text/css" href="%s">'

License
=======

The code is licensed under the `BSD License`_. See the ``LICENSE``
file in the distribution.

.. _`BSD License`: http://www.opensource.org/licenses/bsd-license.php
