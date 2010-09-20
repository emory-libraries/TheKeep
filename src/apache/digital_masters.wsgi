import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'digitalmasters.settings'

# Note that you shouldn't need to set sys.path here if in the apache config
# you pass the python-path option to WSGIDaemonProcess as described in the
# sample config.

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
