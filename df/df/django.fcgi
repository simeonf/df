#!/home3/stevendg/ENV/bin/python

import sys
import os

sys.path.insert(0, '/home3/stevendg/site3.0/df/df')

import env

os.environ['DJANGO_SETTINGS_MODULE'] = 'df.bluehost_settings'

os.environ['DF_DB_PASSWORD'] = env.db_password
from django_fastcgi.servers.fastcgi import runfastcgi
from django.core.servers.basehttp import get_internal_wsgi_application

wsgi_application = get_internal_wsgi_application()
runfastcgi(wsgi_application, method="prefork", daemonize="false", minspare=1, maxspare=5, maxchildren=10)
