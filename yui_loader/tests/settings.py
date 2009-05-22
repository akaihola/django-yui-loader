DATABASE_ENGINE = 'sqlite3'
INSTALLED_APPS = 'yui_loader',
MIDDLEWARE_CLASSES = 'yui_loader.middleware.YUIIncludeMiddleware',
ROOT_URLCONF = 'yui_loader.tests.urls'
YUI_INCLUDE_BASE = '/js/yui/'
