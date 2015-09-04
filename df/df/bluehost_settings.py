import os
from .settings import *

FORCE_SCRIPT_NAME = ''
DEBUG = False
TEMPLATE_DEBUG = False
STATIC_ROOT = '/home3/stevendg/www/new/static'

ALLOWED_HOSTS = ['.decentfilms.com', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'STORAGE_ENGINE': 'InnoDB',
        'NAME': 'stevendg_twopointzero',
        'USER': 'stevendg_two',
        'PASSWORD': os.environ['DF_DB_PASSWORD'],
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
          "init_command": "SET storage_engine=INNODB",
        }
    }
}
