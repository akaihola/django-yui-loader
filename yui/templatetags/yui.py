#!/usr/bin/python
# -*- encoding: utf-8 -*-

from django import template

register = template.Library()

LOADER_URL = 'http://yui.yahooapis.com/2.5.1/build/' \
             'yuiloader/yuiloader-beta-min.js'


def make_script_tag(script, src):
    if src:
        src_attrib = ' src="%s"' % src
    else:
        src_attrib = ''
    return '<script type="text/javascript"%s>%s</script>\n' % (
        src_attrib, script)


def script(script):
    return make_script_tag(script, None)


def script_src(src):
    return make_script_tag('', src)


def context_setdefault(context, varname, value):
    if varname not in context:
        context[varname] = value
    return context[varname]


@register.tag
def YUI(parser, token):
    bits = token.split_contents()[1:]
    if len(bits) < 1:
        raise template.TemplateSyntaxError, \
              'YUI requires at least the command name as an argument'
    cmd = bits.pop(0)
    if cmd == 'loader':
        if bits:
            raise template.TemplateSyntaxError, \
                  'YUI loader takes no arguments'
        return YUILoaderNode()
    elif cmd == 'require':
        nodelist = parser.parse(('endYUI',))
        parser.delete_first_token()
        return YUIRequireNode(bits, nodelist)
    elif cmd == 'alias':
        aliases = [bit.split('=') for bit in bits]
        return YUIAliasNode((varname, module) for varname, module in aliases)
        # todo: tuple extraction error handling
    elif cmd == 'onDOMReady':
        if bits:
            raise template.TemplateSyntaxError, \
                  'YUI onDOMReady takes no arguments'
        nodelist = parser.parse(('endYUI',))
        parser.delete_first_token()
        return YUIOnDomReadyNode(nodelist)

class YUILoaderNode(template.Node):
    def render(self, context):
        if '_yui_loader_initialized' in context:
            return ''
        context['_yui_loader_initialized'] = True
        return ''.join((
            script_src(LOADER_URL),
            script('_DOMReady_funcs=[];'
                   'function _onDOMReady(f){_DOMReady_funcs.push(f);}'),
            YUIRequireNode(['dom', 'event', 'selector'], template.TextNode('for(var i=0;i<_DOMReady_funcs.length;++i)_DOMReady_funcs[i]();_onDOMReady=function(f){f()};')).render(context)))


class YUIRequireNode(template.Node):
    def __init__(self, modules, nodelist=None):
        self.modules = modules
        self.nodelist = nodelist
    def render(self, context):
        #loaded = context_setdefault(context, '_yui_loaded_modules', set())
        #modules = [m for m in self.modules if m not in loaded]
        if self.nodelist is None:
            success_script = ''
        else:
            success_script = self.nodelist.render(context).strip()
        #if not modules:
        #    return script(success_script)
        if success_script:
            on_success = ',onSuccess:function(){%s}' % success_script
        else:
            on_success = ''
        #loaded.update(modules)
        return script(
            '_yui_loader = new YAHOO.util.YUILoader();'
            '_yui_loader.insert({require:[%s]%s});' % (
            ','.join('"%s"' % m for m in self.modules), on_success))


class YUIAliasNode(template.Node):
    def __init__(self, aliases):
        self.aliases = aliases
    def render(self, context):
        assigned = context_setdefault(context, '_yui_assigned_aliases', set())
        assignments = [assignment for assignment in self.aliases
                       if assignment not in assigned]
        if not assignments:
            return ''
        assigned.update(assignments)
        return script('_onDOMReady(function(){%s});' %
                      ''.join('%s=%s;' % (varname, module)
                              for varname, module in assignments))


class YUIOnDomReadyNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context):
        return script('_onDOMReady(%s);') % self.nodelist.render(context)
