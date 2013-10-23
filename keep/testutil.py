"""
Like Voltron, :mod:`keep.testutil` combines the powers of
:mod:`eulfedora.testutil` and :mod:`eulexistdb.testutil` with
file cache swapping into a giant crime-fighting robot.

OK, so maybe not a robot, but it does merge their functionality, and it does
add some of its own: Before starting tests it swaps out the django file
cache so that tests don't stomp on the cache used by other commands. After
testing it swaps the regular cache back into place.
"""

from contextlib import nested
import os
import unittest
from shutil import rmtree
import sunburnt
from mock import Mock

from django.conf import settings
from django.test.simple import DjangoTestSuiteRunner

from eulexistdb import testutil as existdb_testutil
from eulfedora import testutil as fedora_testutil
from eulfedora.server import Repository


def mocksolr_nodupes():
    # set up a mock mock solr query instance to return count of 0 for
    # pre-ingest duplicate checking
    # (NOTE: very nearly duplicate code in keep.file.tests)
    mocksolr_interface = Mock(spec=sunburnt.SolrInterface)
    # mock sunburnt's fluid interface
    mocksolr = mocksolr_interface.return_value
    mocksolr.query.return_value = mocksolr.query
    for method in ['query', 'facet_by', 'sort_by', 'field_limit',
                   'exclude']:
        getattr(mocksolr.query, method).return_value = mocksolr.query
    # set mock solr to indicate no duplicate records
    mocksolr.query.count.return_value = 0
    return mocksolr_interface


class KeepTestCase(existdb_testutil.TestCase):
    def setUp(self):
        super(KeepTestCase, self).setUp()
        self.repo = Repository()

        # NOTE: we should use django.test.utils override_settings for this
        # (not available until django 1.4)
        self._solr_server_url = getattr(settings, 'SOLR_SERVER_URL', None)
        if self._solr_server_url is None:
            # sunburnt solr initialization expects *something* to be set
            settings.SOLR_SERVER_URL = 'http://localhost:919191/solr/'

    def tearDown(self):
        if self._solr_server_url is not None:
            settings.SOLR_SERVER_URL = self._solr_server_url
        else:
            del settings.SOLR_SERVER_URL




class CacheTestWrapper(object):
    # TODO: could this go in eulcommon?
    def __init__(self):
        self.stored_cache_backend = None

    def __enter__(self):
        self.swap_cache()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.restore_cache()

    def swap_cache(self):
        # use a test cache when running tests to avoid conflicts with runserver cache
        cache_backend = getattr(settings, 'CACHE_BACKEND', None)
        if cache_backend and cache_backend.startswith('file://'):
            self.stored_cache_backend = settings.CACHE_BACKEND
            settings.CACHE_BACKEND += '-test'
            print "Switching to test cache: %s" % settings.CACHE_BACKEND

    def restore_cache(self):
        if self.stored_cache_backend:
            cache_backend = settings.CACHE_BACKEND
            # if the cache was used, remove directory & all cache files
            cache_dir = cache_backend[len('file://'):]
            if os.path.exists(cache_dir):
                rmtree(cache_dir)
            settings.CACHE_BACKEND = self.stored_cache_backend
            print "Restoring cache: %s" % settings.CACHE_BACKEND

alternate_test_cache = CacheTestWrapper

class KeepTextTestRunner(unittest.TextTestRunner):
    def run(self, test):
        def wrapped_test(result):
            with nested(fedora_testutil.alternate_test_fedora(),
                    existdb_testutil.alternate_test_existdb(),
                    alternate_test_cache()):
                return test(result)
        return super(KeepTextTestRunner, self).run(wrapped_test)


class KeepTextTestSuiteRunner(DjangoTestSuiteRunner):
    def run_suite(self, suite, **kwargs):
        return KeepTextTestRunner(verbosity=self.verbosity,
                                  failfast=self.failfast).run(suite)


try:
    # when xmlrunner is available, define xml test variants too

    import xmlrunner

    class KeepXmlTestRunner(xmlrunner.XMLTestRunner):
        def __init__(self):
            verbose = getattr(settings, 'TEST_OUTPUT_VERBOSE', False)
            descriptions = getattr(settings, 'TEST_OUTPUT_DESCRIPTIONS', False)
            output = getattr(settings, 'TEST_OUTPUT_DIR', 'test-results')

            super_init = super(KeepXmlTestRunner, self).__init__
            #super_init(verbose=verbose, descriptions=descriptions, output=output)
            super_init(descriptions=descriptions, output=output)

        def run(self, test):
            def wrapped_test(result):
                with nested(fedora_testutil.alternate_test_fedora(),
                        existdb_testutil.alternate_test_existdb(),
                        alternate_test_cache()):
                    return test(result)
            return super(KeepXmlTestRunner, self).run(wrapped_test)

    class KeepXmlTestSuiteRunner(KeepTextTestSuiteRunner):
        def run_suite(self, suite, **kwargs):
            return KeepXmlTestRunner().run(suite)


except ImportError:
    pass
