from django.conf.urls.defaults import *

urlpatterns = patterns('yui_loader.tests.views',

    url('^$', 'test_yui_include'),
)
