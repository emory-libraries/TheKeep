import os
import djcelery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keep.settings')
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
os.environ['HTTP_PROXY'] = 'http://skoda.library.emory.edu:3128/'
os.environ['VIRTUAL_ENV'] = '/home/httpd/keep/env/'

djcelery.setup_loader()

# from django.core.handlers.wsgi import WSGIHandler
# application = WSGIHandler()
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
