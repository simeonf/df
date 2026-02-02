import os

from django.core.wsgi import get_wsgi_application
import dotenv

path = os.path.dirname(os.path.dirname(__file__))
dotenv.load_dotenv(os.path.join(path, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'df.prod_settings')

application = get_wsgi_application()
