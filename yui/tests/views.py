from django.http import HttpResponse

from ambidjangolib.shortcuts import render_rc_response

def test_yui_include(request):
    return render_rc_response(
        'yui/tests/test-yui-include.html',
        request)

