import os
from .settings import *

FORCE_SCRIPT_NAME = ''
DEBUG = True
TEMPLATE_DEBUG = DEBUG
STATIC_ROOT = '/home/decentfilms/public_html/static_new'

ALLOWED_HOSTS = ['.decentfilms.com', 'localhost']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'DEFAULT_STORAGE_ENGINE': 'InnoDB',
        'NAME': 'stevendg_3.0',
        'USER': 'stevendg_3',
        'PASSWORD': os.environ['DF_DB_PASSWORD'],
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
          "init_command": "SET default_storage_engine=INNODB",
        }
    }
}
