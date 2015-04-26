from .settings import *

DEBUG = True
TEMPLATE_DEBUG = True

INSTALLED_APPS += ('debug_toolbar', 'test_without_migrations',)

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

INTERNAL_IPS = ('127.0.0.1',)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': 'unique-snowflake'
    }
}
