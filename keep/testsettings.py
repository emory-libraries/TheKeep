from settings import *

# this setting is needed for unit tests involving celery tasks
# so the test doesn't hang
# NOTE: this setting must be set before other things happen or it doesn't work
CELERY_ALWAYS_EAGER = True


# remove PIDMAN settings - no need to generate PIDs when testing
PIDMAN_HOST = None 
PIDMAN_USER = None 
PIDMAN_PASSWORD = None 
PIDMAN_DOMAIN = None 

# for tests, remove search form context processors
# (otherwise, this adds a solr dependency to every page load)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "keep.version_context", 
)
