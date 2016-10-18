import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'keep.settings'
os.environ['HTTP_PROXY'] = 'http://skoda.library.emory.edu:3128/'
os.environ['VIRTUAL_ENV'] = '/home/httpd/keep/env/'

# Note that you shouldn't need to set sys.path here if in the apache config
# you pass the python-path option to WSGIDaemonProcess as described in the
# sample config.

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "keep.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()