from django.template import RequestContext
from django.shortcuts import render_to_response

def test_yui_include(request):
    return render_to_response(
        'yui/tests/test-yui-include.html',
        {},
        RequestContext(request))

