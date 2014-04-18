from mock import patch, NonCallableMock
from sunburnt import sunburnt

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.test import TestCase

from keep.testutil import KeepTestCase
from keep.audio.models import AudioObject
from keep.search.templatetags import search_tags


@patch('keep.search.views.solr_interface', spec=sunburnt.SolrInterface)
class SearchViewsTest(KeepTestCase):
    # fixtures = ['users'] # TODO: eventually

    @patch('keep.search.views.Paginator', spec=Paginator)
    def test_search(self, mockpaginator, mocksolr_interface):
        search_url = reverse('search:keyword')
        mocksolr = mocksolr_interface.return_value

        mocksolr.query.return_value = mocksolr.query
        for method in ['query', 'facet_by', 'sort_by', 'field_limit',
                       'exclude', 'filter']:
            getattr(mocksolr.query, method).return_value = mocksolr.query

        # testing guest access

        # invalid search term (leading wildcard)
        response = self.client.get(search_url, {'keyword': '*invalid'})
        self.assertContains(response, 'Search terms may not begin with wildcards')

        # search all items
        response = self.client.get(search_url)
        # check solr query args
        # - query should be called with no search terms (find all)
        mocksolr.query.assert_called_with()
        # - sort by title when no search terms for relevance to be meaningful
        mocksolr.query.sort_by.assert_called_with('title')
        # check context params ?

        mocksolr.query.filter.assert_called_with(
            content_model=AudioObject.AUDIO_CONTENT_MODEL,
            has_access_copy=True, researcher_access=True)

        # NOTE: template logic tested separately to avoid
        # complications with callable Mock objects
        testresult = {
            'pid': 'testobj:1',
            'title': 'Something Interesting',
            'collection_source_id': '123',
            'collection_label': 'Papers of Somebody SoandSo',
            'date_created': '1990', 'date_issued': '1991',
            'part': 'Side 1',
            'duration': 65,
            'ark_uri': 'http://pid.co/ark:/1234/53bs4'

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
        self.assertContains(response,
            '<h4>%(collection_source_id)s: %(collection_label)s</h4>' % testresult,
            html=True,
            msg_prefix='collection number and label should both be displayed')
        self.assertContains(response,
            '<p><b>Dates:</b> %(date_issued)s, %(date_created)s</p>' % testresult,
            html=True, msg_prefix='date issued and created should be displayed when present')
        self.assertContains(response, testresult['part'],
            msg_prefix='part note should be displayed when present')
        self.assertContains(response, '1 minute, 5 seconds',
            msg_prefix='duration should be displayed in human-readable form')
        self.assertContains(response, testresult['ark_uri'].replace('http://pid.co/', ''),
            msg_prefix='ARK URI (short-form) should be displayed when present')

        # TODO: test edit link is only present if user has permission to edit


class TestSearchTagsTemplateTags(TestCase):

    def test_ark_id(self):
        self.assertEqual(u'ark:/2534/13j7s',
                         search_tags.ark_id('http://pid.co/ark:/2534/13j7s'))

    def test_ark_noid(self):
        self.assertEqual(u'13j7s',
                         search_tags.ark_noid('http://pid.co/ark:/2534/13j7s'))

    def test_naturl_date(self):
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

