# Django settings for keep project.

import os

# Get the directory of this file for relative dir paths.
# Django sets too many absolute paths.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Absol
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'sitemedia')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, '..', 'sitemedia'),
]
if 'VIRTUAL_ENV' in os.environ:
    STATICFILES_DIRS.append(os.path.join(os.environ['VIRTUAL_ENV'], 'themes', 'genlib'))


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # django default context processors
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
    # additional context processors
    "django.core.context_processors.request",  # always include request in render context
    "keep.collection.context_processors.collection_search",  # collection search form on every page
    "keep.audio.context_processors.item_search",  # audio item search form on every page
    "keep.version_context",  # include app version
    "keep.search.context_processors.search",   # search form on every page
    "keep.common.context_processors.common_settings",  # include selected settings in every page
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'keep.urls'

TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, '..', 'templates'),
]
# also look for templates in virtualenv
if 'VIRTUAL_ENV' in os.environ:
    TEMPLATE_DIRS.extend([
        os.path.join(os.environ['VIRTUAL_ENV'], 'themes', 'genlib'),
        os.path.join(os.environ['VIRTUAL_ENV'], 'src', 'eullocal', 'themes', 'genlib')
    ])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'south',
    'eulexistdb',
    'eulfedora',
    'eulcommon.searchutil',
    'eullocal.django.emory_ldap',
    'eullocal.django.taskresult',
    'eullocal.django.util',
    'keep.accounts',
    'keep.arrangement',
    'keep.audio',
    'keep.collection',
    'keep.common',
    'keep.search',
    'djcelery',
]


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'eullocal.django.emory_ldap.backends.EmoryLDAPBackend',
)

FILE_UPLOAD_HANDLERS = (
    # removing default MemoryFileUploadHandler so all uploaded files can be treated the same
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

# session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'    # use same cache in use elsewhere
SESSION_COOKIE_AGE = 604800   # 1 week (Django default is 2 weeks)
SESSION_COOKIE_SECURE = True  # mark cookie as secure, only transfer via HTTPS
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# using default django login url
LOGIN_URL = '/accounts/login/'

AUTH_PROFILE_MODULE = 'emory_ldap.EmoryLDAPUserProfile'

# the default owner of all fedora objects created by this app
FEDORA_OBJECT_OWNERID = 'thekeep-project'

# mnemonic names for well-known PIDs
PID_ALIASES = {
    'marbl': 'emory:93z53',
    'eua': 'emory:93zd2',
    'oxford': 'emory:b2mx2',
    'pitts': 'emory:93z9n',
    'musicmedia': 'emory:cwtgk',
}

SOLR_SCHEMA = os.path.join(BASE_DIR, '..', 'solr', 'schema.xml')

# Celery Config - standard stuff that will not change from project to project
import djcelery
djcelery.setup_loader()

# explicitly assign a differently-named default queue to prevent
# collisions with other projects using celery (allow celery to create queue for us)
CELERY_ROUTES = {
    'keep.audio.tasks.convert_wav_to_mp3': {'queue': 'keep'}
}

try:
    from keep.localsettings import *
except ImportError:
    import sys
    print >> sys.stderr, 'No local settings. Trying to start, but if ' + \
        'stuff blows up, try copying localsettings.py.dist to ' + \
        'localsettings.py and setting appropriately for your environment.'
    pass

# django_nose configurations

django_nose = None
try:
    # NOTE: errors if DATABASES is not configured (in some cases),
    # so this must be done after importing localsettings
    import django_nose
except ImportError:
    pass

# - only if django_nose is installed, so it is only required for development
if django_nose is not None:
    INSTALLED_APPS.append('django_nose')
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    NOSE_PLUGINS = [
        'eulexistdb.testutil.ExistDBSetUp',
        'eulfedora.testutil.EulfedoraSetUp',
        # ...
    ]
    NOSE_ARGS = ['--with-existdbsetup', '--with-eulfedorasetup']

# disable south migrations in unit tests
SOUTH_TESTS_MIGRATE = False

# override certain settings when running unit tests
if 'DJANGO_TEST_MODE' in os.environ:

    # Context processors to be used for testing
    # - remove search form context processors
    # (otherwise, this adds a solr dependency to every page load)
    TEMPLATE_CONTEXT_PROCESSORS = (
        # django default context processors
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.contrib.messages.context_processors.messages",
        "django.core.context_processors.request",
        "keep.version_context"
    )
    # FIXME: maybe better to use original list and remove problematic ones?

    # this setting is needed for unit tests involving celery tasks
    # so the test doesn't hang
    # NOTE: this setting must be set before other things happen or it doesn't work
    CELERY_ALWAYS_EAGER = True

    # remove PIDMAN settings - no need to generate PIDs when testing
    PIDMAN_HOST = None
    PIDMAN_USER = None
    PIDMAN_PASSWORD = None
    PIDMAN_DOMAIN = None

