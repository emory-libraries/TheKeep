# Django settings for keep project.

import os

# Get the directory of this file for relative dir paths.
# Django sets too many absolute paths.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# NOTE: user media unused in this site,
# so MEDIA_ROOT and MEDIA_URL are not set

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

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
    "django.core.context_processors.static",
    "eultheme.context_processors.template_settings",
    "eultheme.context_processors.downtime_context",
    "keep.collection.context_processors.collection_search",  # collection search form on every page
    "keep.audio.context_processors.item_search",  # audio item search form on every page
    "keep.version_context",  # include app version
    "keep.repoadmin.context_processors.search",   # search form on every page
    'keep.accounts.context_processors.researcher_no_analytics'
)
# NOTE: if you modify the configured context processors and need
# a new processor included in unit tests, be sure to update
# the list in keep.testplugins.KeepTestSettings


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'eultheme.middleware.DownpageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'keep.accounts.middleware.ResearcherAccessMiddleware',
    'keep.search.middleware.UnsupportedBrowserMiddleware',
)

ROOT_URLCONF = 'keep.urls'

TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, '..', 'templates'),
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # bootstrap django-admin - must be loaded before admin
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'djcelery',
    'widget_tweaks',
    'eulexistdb',
    'eulfedora',
    'eulcommon.searchutil',
    # emory_ldap included to migrate back to auth.User;
    # should be removed in the next version
    'eullocal.django.emory_ldap',
    'eullocal.django.taskresult',
    'eultheme',
    'downtime',
    'keep.accounts',
    'keep.arrangement',
    'keep.audio',
    'keep.video',
    'keep.collection',
    'keep.common',
    'keep.repoadmin',
    'keep.file',
    'keep.search',
]


AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

FILE_UPLOAD_HANDLERS = (
    # removing default MemoryFileUploadHandler so all uploaded files can be treated the same
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

# session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'    # use same cache in use elsewhere
SESSION_COOKIE_AGE = 604800   # 1 week (Django default is 2 weeks)
# SESSION_COOKIE_SECURE = True  # mark cookie as secure, only transfer via HTTPS
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# using default django login url
LOGIN_URL = '/accounts/login/'

# the default owner of all fedora objects created by this app
FEDORA_OBJECT_OWNERID = 'thekeep-project'

# mnemonic names for well-known PIDs
PID_ALIASES = {
    'marbl': 'emory:93z53',
    'eua': 'emory:93zd2',
    'oxford': 'emory:b2mx2',
    'pitts': 'emory:93z9n',
    'musicmedia': 'emory:cwtgk',
    'etd': 'emory:pgfch',
    'health': 'emory:pq6rs',
}

# urls that should be accessible during configured downtime periods
DOWNTIME_EXEMPT_PATHS = (
   '/db-admin',
   '/admin',
   '/indexdata'
)

SOLR_SCHEMA = os.path.join(BASE_DIR, '..', 'solr', 'schema.xml')

# Celery Config - standard stuff that will not change from project to project
import djcelery
djcelery.setup_loader()

# explicitly assign a differently-named default queue to prevent
# collisions with other projects using celery (allow celery to create queue for us)
CELERY_ROUTES = {
    'keep.audio.tasks.convert_wav_to_mp3': {'queue': 'keep'}
}
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'


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
        'keep.testplugins.KeepTestSettings',
    ]
    NOSE_ARGS = ['--with-existdbsetup', '--with-eulfedorasetup',
        '--with-keeptestsettings']

# disable south migrations in unit tests
SOUTH_TESTS_MIGRATE = False
