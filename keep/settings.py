# Django settings for keep project.

from os import path

# Get the directory of this file for relative dir paths.
# Django sets too many absolute paths.
BASE_DIR = path.dirname(path.abspath(__file__))

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = path.join(BASE_DIR, '..', 'sitemedia')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # django default context processors
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
    # additional context processors
    "django.core.context_processors.request", # always include request in render context
    "keep.collection.context_processors.collection_search",  # collection search form on every page
    "keep.audio.context_processors.item_search",  # audio item search form on every page
    "keep.version_context", # include app version
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
    path.join(BASE_DIR, '..', 'templates'),
]

# also look for templates in virtualenv
import os
if 'VIRTUAL_ENV' in os.environ:
    genlib_path = os.path.join(os.environ['VIRTUAL_ENV'], 'themes', 'genlib')
    TEMPLATE_DIRS.append(genlib_path)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'eulexistdb',
    'eulfedora',
    'eullocal.django.emory_ldap',
    'eullocal.django.taskresult',
    'eullocal.django.util',
    'keep.accounts',
    'keep.audio',
    'keep.collection',
    'keep.common',
    'keep.old_dm',
    'djcelery',
)


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'eullocal.django.emory_ldap.backends.EmoryLDAPBackend',
)

FILE_UPLOAD_HANDLERS = (
    # removing default MemoryFileUploadHandler so all uploaded files can be treated the same
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

# custom router to make old_dm database is only used for old_dm models & vice versa
DATABASE_ROUTERS = ['keep.old_dm.db.OldDMRouter']

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

# Celery Config - standard stuff that will not change from project to project
import djcelery
djcelery.setup_loader()
# use a differently-named default queue to keep separate from other projects using celery
CELERY_DEFAULT_QUEUE = 'keep'


try:
    from localsettings import *
except ImportError:
    import sys
    print >>sys.stderr, 'No local settings. Trying to start, but if ' + \
        'stuff blows up, try copying localsettings.py.sample to ' + \
        'localsettings.py and setting appropriately for your environment.'
    pass

import sys
try:
    sys.path.extend(EXTENSION_DIRS)
except NameError:
    pass # EXTENSION_DIRS not defined. This is OK; we just won't use it.
del sys

try:
    # use xmlrunner if it's installed; default runner otherwise. download
    # it from http://github.com/danielfm/unittest-xml-reporting/ to output
    # test results in JUnit-compatible XML.
    import xmlrunner
    TEST_RUNNER='keep.testutil.KeepXmlTestSuiteRunner'
    TEST_OUTPUT_DIR='test-results'
except ImportError:
    pass

