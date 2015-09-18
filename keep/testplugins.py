import sys
from nose.plugins.base import Plugin
from django.conf import settings

class KeepTestSettings(Plugin):

    def begin(self):
        # Context processors to be used for testing
        # - remove search form context processors
        # (otherwise, this adds a solr dependency to every page load)
        print >> sys.stderr, 'Overriding settings ' + \
            '(template context processors, celery always eager, disabling pidmanager)'
        settings.TEMPLATE_CONTEXT_PROCESSORS = (
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
        settings.CELERY_ALWAYS_EAGER = True

        # remove PIDMAN settings - no need to generate PIDs when testing
        settings.PIDMAN_HOST = None
        settings.PIDMAN_USER = None
        settings.PIDMAN_PASSWORD = None
        settings.PIDMAN_DOMAIN = None
        # pidmanager has already been initialized at this point,
        # so override it
        from keep.common import fedora
        fedora.pidman = None

    def finalize(self, result):
        # do we need to restore any of these settings?
        pass

    def help(self):
        return 'Customize settings for running tests.'
