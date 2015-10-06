"""
Like Voltron, :mod:`keep.testutil` combines the powers of
:mod:`eulfedora.testutil` and :mod:`eulexistdb.testutil` with
file cache swapping into a giant crime-fighting robot.

OK, so maybe not a robot, but it does merge their functionality, and it does
add some of its own: Before starting tests it swaps out the django file
cache so that tests don't stomp on the cache used by other commands. After
testing it swaps the regular cache back into place.
"""

import sunburnt
from mock import Mock

from django.conf import settings
# from django.test.simple import DjangoTestSuiteRunner

from eulexistdb import testutil as existdb_testutil
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

