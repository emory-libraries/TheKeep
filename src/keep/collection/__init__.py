# keep.collection makes use of django caching
# Use test signals to swap out the default configured cache with a
# test cache that will be used only for the duration of the test.

from shutil import rmtree

from django.conf import settings

from eulcore.django.testsetup import starting_tests, finished_tests


def _swap_cache(sender, **kwargs):
    # use a test cache when running tests to avoid conflicts with runserver cache
    cache_backend = getattr(settings, 'CACHE_BACKEND', None)
    if cache_backend and cache_backend.startswith('file://'):
        settings.CACHE_BACKEND += '-test'
        print "Switching to test cache : %s" % settings.CACHE_BACKEND


def _restore_cache(sender, **kwargs):
    cache_backend = getattr(settings, 'CACHE_BACKEND', None)
    if cache_backend and cache_backend.startswith('file://') \
    	and cache_backend.endswith('-test'):
        # remove the cache directory & all cache files under it
        rmtree(cache_backend[len('file://'):])
        settings.CACHE_BACKEND = cache_backend[:len(cache_backend) - len('-test')]
        print "Restoring cache : %s" % settings.CACHE_BACKEND


starting_tests.connect(_swap_cache)
finished_tests.connect(_restore_cache)
