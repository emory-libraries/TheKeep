from mock import patch, NonCallableMock, MagicMock
from sunburnt import sunburnt

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.test import TestCase

from keep.testutil import KeepTestCase
from keep.accounts.models import ResearcherIP
from keep.audio.models import AudioObject
from keep.search.templatetags import search_tags
from keep.common.utils import solr_interface


@patch('keep.search.forms.SearchForm.library_choices_by_user')
@patch('keep.search.views.solr_interface', spec=sunburnt.SolrInterface)
class SearchViewsTest(KeepTestCase):
    # fixtures = ['users'] # TODO: eventually

    @patch('keep.search.views.Paginator', spec=Paginator)
    def test_search(self, mockpaginator, mocksolr_interface, mocksearch_libs):
        search_url = reverse('search:keyword')
        mocksolr = mocksolr_interface.return_value

        mocksolr.query.return_value = mocksolr.query
        for method in ['query', 'facet_by', 'sort_by', 'field_limit',
                       'exclude', 'filter']:
            getattr(mocksolr.query, method).return_value = mocksolr.query

        # testing guest access - should be denied
        response = self.client.get(search_url, {'keyword': '*invalid'})
        expected, got = 302, response.status_code
        self.assertEqual(expected, got,
            'Expected status code %s when accessing %s as guest, got %s' % \
            (expected, got,search_url))
        self.assert_(reverse('accounts:login') in response['Location'],
            'guest access to search should redirect to login page')

        # create researcher IP for localhost so anonymous access will be
        # treated as anonymous researcher
        researchip = ResearcherIP(name='test client', ip_address='127.0.0.1')
        researchip.save()

        # invalid search term (leading wildcard)
        response = self.client.get(search_url, {'keyword': '*invalid'})
        self.assertContains(response, 'Search terms may not begin with wildcards')

        # search all items
        response = self.client.get(search_url)
        # check solr query args
        # - query should be called with no search terms (find all)
        mocksolr.query.assert_called_with()
        # - sort by title when no search terms for relevance to be meaningful
        mocksolr.query.sort_by.assert_called_with('title_exact')
        # check context params ?

        mocksolr.query.filter.assert_called_with(
            content_model=AudioObject.AUDIO_CONTENT_MODEL,
            has_access_copy=True, researcher_access=True)

        # NOTE: template logic tested separately to avoid
        # complications with callable Mock objects
        testresult = {
            'pid': 'testobj:1',
            'title': 'Something Interesting',
            'collection_id': 'testcoll:123',
            'collection_source_id': '123',
            'collection_label': 'Papers of Somebody SoandSo',
            'date_created': '1990', 'date_issued': '1991',
            'part': 'Side 1',
            'duration': 65,
            'ark_uri': 'http://pid.co/ark:/1234/53bs4',


        }

        # use a noncallable for the pagination result that is used in the template
        # because passing callables into django templates does weird things
        mockpage = NonCallableMock()
        mockpaginator.return_value.page.return_value = mockpage
        mockpage.object_list = [testresult]
        mockpage.has_other_pages = False
        mockpage.paginator.count = 1
        mockpage.paginator.page_range = [1]

        # search with search terms
        response = self.client.get(search_url, {'keyword': 'fantabulous expurgation'})
        # check solr query args
        # - query should be called with tokenized search terms
        mocksolr.query.query.assert_called_with('fantabulous', 'expurgation')
        # - sort by relevance score when there are search terms
        mocksolr.query.sort_by.assert_called_with('-score')
        # - include relevance score in return values
        mocksolr.query.field_limit.assert_called_with(score=True)

        # test object info displayed on search result page from mock result
        self.assertContains(response, reverse('audio:view', args=[testresult['pid']]),
            msg_prefix='search result links to audio view page')
        self.assertContains(response, testresult['title'],
            msg_prefix='search result displays audio object title')
        # add expected url to test result dict to simplify testing
        testresult['url'] =  reverse('collection:view', kwargs={'pid': testresult['collection_id']})
        self.assertContains(response,
            '<h4><a class="text-muted" href="%(url)s">%(collection_source_id)s: %(collection_label)s</a></h4>' % \
            testresult,
            html=True,
            msg_prefix='collection number and label should both be displayed')
        self.assertContains(response,
            '<li><h4>Issued</h4><span>%(date_issued)s</span></li>' % testresult,
            html=True, msg_prefix='date issued and should be displayed when present')
        self.assertContains(response,
            '<li><h4>Created</h4><span>%(date_created)s</span></li>' % testresult,
            html=True, msg_prefix='date issued and should be displayed when present')
        self.assertContains(response, testresult['part'],
            msg_prefix='part note should be displayed when present')
        self.assertContains(response, '1 minute, 5 seconds',
            msg_prefix='duration should be displayed in human-readable form')
        self.assertContains(response, testresult['ark_uri'].split('/')[-1],
            msg_prefix='ARK NOID should be displayed when present')

        # TODO: test edit link is only present if user has permission to edit

        researchip.delete()

    @patch('keep.search.views.Paginator', spec=Paginator)
    def test_search_collections(self, mockpaginator, mocksolr_interface, mocksearch_libs):
        solr = solr_interface()
        search_url = reverse('search:keyword')
        mocksolr = mocksolr_interface.return_value
        mocksolr.Q = MagicMock(solr.Q)

        mocksolr.query.return_value = mocksolr.query
        for method in ['query', 'facet_by', 'sort_by', 'field_limit',
                       'exclude', 'filter']:
            getattr(mocksolr.query, method).return_value = mocksolr.query


        # create researcher IP for localhost so anonymous access will be
        # treated as anonymous researcher
        researchip = ResearcherIP(name='test client', ip_address='127.0.0.1')
        researchip.save()


        response = self.client.get(search_url, {'collection': '1000'})
        # check solr query args
        # - collection should trigger OR query against collection label and number fields
        mocksolr.Q.assert_any_call(collection_label='1000')
        mocksolr.Q.assert_any_call(collection_source_id='1000')
        # NOTE: not checking OR query direclty because unclear how to replicate in mock

        self.assertContains(response,
            '<input class="form-control" id="id_collection" name="collection" placeholder="Search by collection name or number" type="text" value="%s">' % \
            '1000',
            html=True,
            msg_prefix='collection search value should be displayed on result page via form')

        researchip.delete()

    @patch('keep.search.views.Paginator', spec=Paginator)
    def test_search_bydate(self, mockpaginator, mocksolr_interface, mocksearch_libs):
        solr = solr_interface()
        search_url = reverse('search:keyword')
        mocksolr = mocksolr_interface.return_value
        mocksolr.Q = MagicMock(solr.Q)

        mocksolr.query.return_value = mocksolr.query
        for method in ['query', 'facet_by', 'sort_by', 'field_limit',
                       'exclude', 'filter']:
            getattr(mocksolr.query, method).return_value = mocksolr.query

        # create researcher IP for localhost so anonymous access will be
        # treated as anonymous researcher
        researchip = ResearcherIP(name='test client', ip_address='127.0.0.1')
        researchip.save()

        # start date only
        sdate = '1980'
        response = self.client.get(search_url, {'start_date': sdate})
        # check solr query args
        # - date should query dates created and issued explicitly
        mocksolr.Q.assert_any_call(date_created__gte=sdate)
        mocksolr.Q.assert_any_call(date_issued__gte=sdate)

        self.assertContains(response,
            '<input class="form-control" id="id_start_date" name="start_date" placeholder="Start year" type="tel" value="%s">' % sdate,
            html=True,
            msg_prefix='start date search value should be displayed on result page via form')

        # end date only
        edate = '2001'
        response = self.client.get(search_url, {'end_date': edate})
        # check solr query args
        # - date should query dates created and issued explicitly
        search_edate = '%s-12-31' % edate
        mocksolr.Q.assert_any_call(date_created__lte=search_edate)
        mocksolr.Q.assert_any_call(date_issued__lte=search_edate)

        self.assertContains(response,
            '<input class="form-control" id="id_end_date" name="end_date" placeholder="End year" type="tel" value="%s">' % edate,
            html=True,
            msg_prefix='start date search value should be displayed on result page via form')

        # start and end date together
        response = self.client.get(search_url, {'start_date': sdate, 'end_date': edate})
        # check solr query args
        # - date should query dates created and issued explicitly
        mocksolr.Q.assert_any_call(date_created__range=(sdate, search_edate))
        mocksolr.Q.assert_any_call(date_issued__range=(sdate, search_edate))

        researchip.delete()

    @patch('keep.search.views.Paginator', spec=Paginator)
    def test_search_bylibrary(self, mockpaginator, mocksolr_interface, mocksearch_libs):
        solr = solr_interface()
        search_url = reverse('search:keyword')
        mocksolr = mocksolr_interface.return_value
        mocksolr.Q = MagicMock(solr.Q)

        mocksolr.query.return_value = mocksolr.query
        for method in ['query', 'facet_by', 'sort_by', 'field_limit',
                       'exclude', 'filter', 'join']:
            getattr(mocksolr.query, method).return_value = mocksolr.query

        # create researcher IP for localhost so anonymous access will be
        # treated as anonymous researcher
        researchip = ResearcherIP(name='test client', ip_address='127.0.0.1')
        researchip.save()

        # NOTE: currently uses info:fedora/ pid format for select, so use that here
        libpid = 'info:fedora/%s' % settings.PID_ALIASES['marbl']
        marbl_name = 'Manuscript, Archives, and Rare Book Library'
        # set mock list of library choices to include our test value so form will be valid
        mocksearch_libs.return_value = [(libpid, marbl_name)]
        response = self.client.get(search_url, {'library': libpid})
        # check solr query args
        # - date should query dates created and issued explicitly
        mocksolr.query.join.assert_called_with('pid', 'collection_id', archive_id=libpid)

        self.assertContains(response,
            '<option value="%s" selected="selected">%s</option>' % (libpid, marbl_name),
            html=True,
            msg_prefix='library filter should be selected on result page form')


class TestSearchTagsTemplateTags(TestCase):

    def test_ark_id(self):
        self.assertEqual(u'ark:/2534/13j7s',
                         search_tags.ark_id('http://pid.co/ark:/2534/13j7s'))

    def test_ark_noid(self):
        self.assertEqual(u'13j7s',
                         search_tags.ark_noid('http://pid.co/ark:/2534/13j7s'))

    def test_natural_date(self):
        # year only
        self.assertEqual('1980',
                         search_tags.natural_date('1980'))
        self.assertEqual('1980',
                         search_tags.natural_date('1980-00-00'))

        self.assertEqual('May 1964',
                         search_tags.natural_date('1964-05'))
        self.assertEqual('May 1964',
                         search_tags.natural_date('1964-05-00'))

        self.assertEqual('Apr 01, 1973',
                         search_tags.natural_date('1973-04-01'))

