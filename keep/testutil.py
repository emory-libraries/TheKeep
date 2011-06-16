"""
Like Voltron, :mod:`keep.testutil` combines the powers of
:mod:`eulfedora.testutil` and :mod:`eulexistdb.testutil` with
file cache swapping into a giant crime-fighting robot.

OK, so maybe not a robot, but it does merge their functionality, and it does
add some of its own: Before starting tests it swaps out the django file
cache so that tests don't stomp on the cache used by other commands. After
testing it swaps the regular cache back into place.
"""

import os
import unittest
from shutil import rmtree

from django.conf import settings
from django.test.simple import DjangoTestSuiteRunner

from eulexistdb import testutil as existdb_testutil
from eulfedora import testutil as fedora_testutil

KeepTestCase = existdb_testutil.TestCase

class KeepTestResult(fedora_testutil.FedoraTestResult,
                     existdb_testutil.ExistDBTestResult):

    def startTestRun(self):
        super(KeepTestResult, self).startTestRun()
        self._swap_cache()

    def stopTestRun(self):
        self._restore_cache()
        super(KeepTestResult, self).stopTestRun()

    def _swap_cache(self):
        # use a test cache when running tests to avoid conflicts with runserver cache
        cache_backend = getattr(settings, 'CACHE_BACKEND', None)
        self._stored_cache_backend = None
        if cache_backend and cache_backend.startswith('file://'):
            self._stored_cache_backend = settings.CACHE_BACKEND
            settings.CACHE_BACKEND += '-test'
            print "Switching to test cache: %s" % settings.CACHE_BACKEND

    def _restore_cache(self):
        if self._stored_cache_backend:
            cache_backend = settings.CACHE_BACKEND
            # if the cache was used, remove directory & all cache files 
            cache_dir = cache_backend[len('file://'):]
            if os.path.exists(cache_dir):
                rmtree(cache_dir)
            settings.CACHE_BACKEND = self._stored_cache_backend
            print "Restoring cache: %s" % settings.CACHE_BACKEND


class KeepTestSuiteRunner(DjangoTestSuiteRunner):
    def run_suite(self, suite, **kwargs):
        return unittest.TextTestRunner(resultclass=KeepTestResult,
                                       verbosity=self.verbosity,
                                       failfast=self.failfast).run(suite)


try:
    # when xmlrunner is available, define xml test variants too

    import xmlrunner

    class KeepXmlTestResult(fedora_testutil.FedoraXmlTestResult,
                            existdb_testutil.ExistDBXmlTestResult):
        def __init__(self, **kwargs):
            fedora_testutil.FedoraXmlTestResult.__init__(self, **kwargs)
            existdb_testutil.ExistDBXmlTestResult.__init__(self, **kwargs)


    class KeepXmlTestRunner(xmlrunner.XMLTestRunner):
        def _make_result(self):
            return KeepXmlTestResult(stream=self.stream,
                                     descriptions=self.descriptions,
                                     verbosity=self.verbosity,
                                     elapsed_times=self.elapsed_times)


    class KeepXmlTestSuiteRunner(DjangoTestSuiteRunner):
        def run_suite(self, suite, **kwargs):
            settings.DEBUG = False
            verbose = getattr(settings, 'TEST_OUTPUT_VERBOSE', False)
            descriptions = getattr(settings, 'TEST_OUTPUT_DESCRIPTIONS', False)
            output = getattr(settings, 'TEST_OUTPUT_DIR', '.')

            # call roughly the way that xmlrunner does, with our customized test runner
            return KeepXmlTestRunner(verbose=verbose,
                                     descriptions=descriptions,
                                     output=output).run(suite)

except ImportError:
    pass
