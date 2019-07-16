import os
from .settings import *

FORCE_SCRIPT_NAME = ''
DEBUG = False
TEMPLATE_DEBUG = False
STATIC_ROOT = '/home/stevendg/www/static_new'

ALLOWED_HOSTS = ['.decentfilms.com', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'STORAGE_ENGINE': 'InnoDB',
        'NAME': 'stevendg_3.0',
        'USER': 'stevendg_3',
        'PASSWORD': os.environ['DF_DB_PASSWORD'],
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
          "init_command": "SET storage_engine=INNODB",
        }
    }
}
