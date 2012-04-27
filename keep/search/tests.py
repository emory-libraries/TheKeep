from django import forms
from django.core.urlresolvers import reverse
from django.test import TestCase
from mock import patch, Mock, call
from sunburnt import sunburnt

from keep.search.forms import SolrSearchField
from keep.testutil import KeepTestCase
from keep.audio.tests import ADMIN_CREDENTIALS

class SolrSearchFieldTest(TestCase):

    def setUp(self):
        self.field = SolrSearchField(required=True)

    def test_to_python(self):
        self.assert_(isinstance(self.field.to_python(''), list),
                     'to python should return a list, even for an empty value')
        self.assert_(isinstance(self.field.to_python('one two three'), list),
                     'to python should return a list')

    def test_validate(self):
        # inherited validation - required field error
        self.assertRaises(forms.ValidationError,
                          self.field.validate, [])

        # when not required: empty should be valid
        not_req = SolrSearchField(required=False)
        not_req.validate([])

        # no validation error should be raised 
        self.field.validate([(None, 'one'), (None, 'two')])
        self.field.validate([(None, 'one'), (None, 'two'),
                             (None, '"three four"')])
        self.field.validate([(None, 'one'), ('title', 'two'),
                             (None, '"three *four"')])

        # validation errors should be raised
        self.assertRaises(forms.ValidationError,
                          self.field.validate, [(None, '*foo')])
        self.assertRaises(forms.ValidationError,
                          self.field.validate, [(None, 'foo'),
                                                ('title', '*bar')])
        self.assertRaises(forms.ValidationError,
                          self.field.validate, [('text', '"foo bar"'),
                                                (None, '*baz')])


@patch('keep.search.views.solr_interface', spec=sunburnt.SolrInterface)
class SearchViewsTest(KeepTestCase):
    fixtures =  ['users']

    @patch('keep.search.views.Paginator')
    def test_search(self, mockpaginator, mocksolr_interface):
        search_url = reverse('search:keyword')
        mocksolr = mocksolr_interface.return_value

        mocksolr.query.return_value = mocksolr.query
        for method in ['query', 'facet_by', 'sort_by', 'field_limit']:
            getattr(mocksolr.query, method).return_value = mocksolr.query

        # no guest access
        # TODO: should redirect to local login, not django admin login
        #response = self.client.get(search_url, follow=False)
        #self.assertEqual(303, response.status_code)
        

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # invalid search term (leading wildcard)
        response = self.client.get(search_url, {'keyword': '*invalid'})
        self.assertContains(response, 'Search terms may not begin with wildcards')

        # test search result content with one of each type
        content = [
            {'pid': 'audio:1', 'object_type': 'audio', 'title': 'recording'},
            {'pid': 'coll:1', 'object_type': 'collection', 'title': 'mss 123',
             'dsids': ['MODS'],},
            {'pid': 'scoll:1', 'object_type': 'collection', 'title': 'process batch',},
            {'pid': 'boda:1', 'object_type': 'born-digital', 'title': 'email'}
        ]
        # construct a minimal mock page object to test the template, since
        # django templates don't deal with callable Mock objects well 
        class MockPage(object):
            object_list = []
        page = MockPage()
        page.object_list = content
        mockpaginator.return_value.page.return_value = page

        # search all items
        response = self.client.get(search_url)
        # check solr query args
        # - query should be called with no search terms (find all)
        mocksolr.query.assert_called_with() 
        # - sort by created when no search terms for relevance to be meaningful
        mocksolr.query.sort_by.assert_called_with('-created')
        # check context params ?

        # test response content
        self.assertContains(response, 'sorted by date uploaded')
        
        self.assertContains(response, reverse('audio:edit',
                                              kwargs={'pid': 'audio:1'}),
             msg_prefix='search results should link to audio edit form for audio item')
        # TODO: test both simple and regular collections
        self.assertContains(response, reverse('collection:edit',
                                              kwargs={'pid': 'coll:1'}),
             msg_prefix='search results should link to collection edit form for collection')
        self.assertContains(response, reverse('collection:simple_edit',
                                              kwargs={'pid': 'scoll:1'}),
             msg_prefix='search results should link to simple collection edit form for simple collection')
        self.assertContains(response, reverse('arrangement:edit',
                                              kwargs={'pid': 'boda:1'}),
             msg_prefix='search results should link to arrangement edit form for arrangement object')

        # at minimum, item titles should display
        for item in content:
            self.assertContains(response, item['title'],
                msg_prefix='search results should contain item title "%s"' % \
                                item['title'])


        # search with search terms
        response = self.client.get(search_url, {'keyword': 'fantabulous expurgation'})
        # check solr query args
        # - query should be called with tokenized search terms 
        mocksolr.query.assert_called_with('fantabulous', 'expurgation') 
        # - sort by score then by date created when there are search terms
        sort_args = mocksolr.query.sort_by.call_args_list[-2:]
        self.assertEqual(call('-score'), sort_args[0])
        self.assertEqual(call('-created'), sort_args[1])
        # - include relevance score in return values
        mocksolr.query.field_limit.assert_called_with(score=True)

        self.assertContains(response, 'fantabulous',
            msg_prefix='search term should be displayed on results page')
        self.assertContains(response, 'expurgation',
            msg_prefix='search term should be displayed on results page')
        self.assertContains(response, 'sorted by relevance')

