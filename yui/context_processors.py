from django.conf import settings

def yui(request):
    return {'YUI_INCLUDE_BASE': settings.YUI_INCLUDE_BASE}
