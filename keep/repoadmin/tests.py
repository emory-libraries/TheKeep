import logging
from django import forms
from django.http import HttpRequest
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.test import TestCase
import json
from mock import patch, Mock, call
from sunburnt import sunburnt
from keep.arrangement.models import ArrangementObject
from keep.audio.models import AudioObject
from keep.collection.models import SimpleCollection

from keep.repoadmin.forms import SolrSearchField, KeywordSearch
from keep.testutil import KeepTestCase
from keep.audio.tests import ADMIN_CREDENTIALS

logger = logging.getLogger(__name__)


class SolrSearchFieldTest(TestCase):

    def setUp(self):
        self.field = SolrSearchField(required=True)

    def test_to_python(self):
        self.assert_(isinstance(self.field.to_python(''), list),
                     'to python should return a list, even for an empty value')
        self.assert_(isinstance(self.field.to_python('one two three'), list),
                     'to python should return a list')

        # validation error should be raised if parsing fails
        with patch('keep.repoadmin.forms.parse_search_terms') as pst:
            pst.side_effect = Exception
            self.assertRaises(forms.ValidationError,
                              self.field.to_python, 'one:two:three')

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


@patch('keep.repoadmin.views.solr_interface', spec=sunburnt.SolrInterface)
class RepoAdminViewsTest(KeepTestCase):
    fixtures = ['users']

    def setUp(self):
        #get user
        self.user = get_user_model().objects.get(username=ADMIN_CREDENTIALS['username'])
        self.audio_perm = Permission.objects.get(codename='marbl_allowed')
        self.bd_perm = Permission.objects.get(codename='arrangement_allowed')

    def tearDown(self):
        #rest user to superuser after test
        self.user.user_permissions.clear()
        self.user.is_superuser = True
        self.user.save()

    @patch('keep.repoadmin.views.Paginator')
    def test_search(self, mockpaginator, mocksolr_interface):
        search_url = reverse('repo-admin:search')
        mocksolr = mocksolr_interface.return_value

        mocksolr.query.return_value = mocksolr.query
        for method in ['query', 'facet_by', 'sort_by', 'field_limit',
                       'filter', 'exclude']:
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

        # search all items
        response = self.client.get(search_url)
        # check solr query args
        # - query should be called with no search terms (find all)
        mocksolr.query.assert_called_with()
        # - sort by created when no search terms for relevance to be meaningful
        mocksolr.query.sort_by.assert_called_with('-created')
        # check context params ?

        # NOTE: template logic tested separately to avoid
        # complications with callable Mock objects

        # search with search terms
        response = self.client.get(search_url, {'keyword': 'fantabulous expurgation'})
        # check solr query args
        # - query should be called with tokenized search terms
        mocksolr.query.query.assert_called_with('fantabulous', 'expurgation')
        # - sort by score then by date created when there are search terms
        sort_args = mocksolr.query.sort_by.call_args_list[-2:]
        self.assertEqual(call('-score'), sort_args[0])
        self.assertEqual(call('-created'), sort_args[1])
        # - include relevance score in return values
        # NOTE: not testing via assert_called_with because now sunburnt
        # seems to require a full list of all fields to return
        args, kwargs = mocksolr.query.field_limit.call_args
        self.assertTrue(kwargs['score'], 'relevance score should be returned from solr')
        # mocksolr.query.field_limit.assert_called_with(score=True)

        # NOTE: no longer testing content filtering based on permissions,
        # since that logic is now handled in accounts.utils.filter_by_perms
        # and is not specific to this view

    @patch('keep.repoadmin.views.Paginator')
    def test_search_by_user(self, mockpaginator, mocksolr_interface):
        search_url = reverse('repo-admin:search')
        mocksolr = mocksolr_interface.return_value

        mocksolr.query.return_value = mocksolr.query
        for method in ['query', 'facet_by', 'sort_by', 'field_limit', 'filter', 'exclude']:
            getattr(mocksolr.query, method).return_value = mocksolr.query

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # search by user
        self.client.get(search_url, {'keyword': 'user:admin'})
        # check solr query args
        # - query should be called with tokenized search terms
        mocksolr.query.query.assert_any_call(users='admin')
        # - sort by score then date when fielded search terms
        sort_args = mocksolr.query.sort_by.call_args_list[-2:]
        self.assertEqual(call('-created'), sort_args[0])

        # search by creator/ingester
        self.client.get(search_url, {'keyword': 'added_by:one'})
        mocksolr.query.query.assert_any_call(added_by='one')

        # multiple values for a single field
        self.client.get(search_url, {'keyword': 'user:bob user:jane'})
        mocksolr.query.query.assert_any_call(users='bob')
        mocksolr.query.query.assert_any_call(users='jane')

        # incomplete field
        self.client.get(search_url, {'keyword': 'user:'})
        mocksolr.query.query.assert_called_with('user:')

        # unknown field
        self.client.get(search_url, {'keyword': 'foo:bar'})
        mocksolr.query.query.assert_called_with('foo:bar')

    @patch('keep.repoadmin.views.Paginator')
    def test_search_by_coll(self, mockpaginator, mocksolr_interface):
        search_url = reverse('repo-admin:search')
        mocksolr = mocksolr_interface.return_value

        mocksolr.query.return_value = mocksolr.query
        for method in ['query', 'facet_by', 'sort_by', 'field_limit', 'filter', 'exclude']:
            getattr(mocksolr.query, method).return_value = mocksolr.query

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # search by coll (collection) label
        self.client.get(search_url, {'keyword': 'coll:kittens'})
        # check solr query args
        # - query should be called with tokenized search terms
        mocksolr.query.query.assert_any_call(collection_label='kittens')
        # - sort by date created wheno only using fielded search terms
        logger.info("SORT: %s" % mocksolr.query.sort_by.call_args_list)
        sort_args = mocksolr.query.sort_by.call_args_list[-2:]
        self.assertEqual(call('-created'), sort_args[0])

        # search by coll (collection) source_id
        self.client.get(search_url, {'keyword': 'coll:200'})
        # check solr query args
        # - query should be called with tokenized search terms
        mocksolr.query.query.assert_any_call(collection_source_id='200')

        # search by collection with keyword
        self.client.get(search_url, {'keyword': 'coll:kittens siamese'})
        # check solr query args
        # - query should be called with tokenized search terms
        mocksolr.query.query.assert_any_call(collection_label='kittens')
        # - sort by score, then date created
        sort_args = mocksolr.query.sort_by.call_args_list[-2:]
        self.assertEqual(call('-score'), sort_args[0])
        self.assertEqual(call('-created'), sort_args[1])
        # - include relevance score in return values
        # NOTE: not testing via assert_called_with because now sunburnt
        # seems to require a full list of all fields to return
        # mocksolr.query.field_limit.assert_called_with(score=True)
        args, kwargs = mocksolr.query.field_limit.call_args
        self.assertTrue(kwargs['score'], 'relevance score should be returned from solr')

    @patch('keep.repoadmin.views.Paginator')
    def test_search_facets(self, mockpaginator, mocksolr_interface):
        # test facet logic in the search
        search_url = reverse('repo-admin:search')
        mocksolr = mocksolr_interface.return_value

        mocksolr.query.return_value = mocksolr.query
        for method in ['query', 'facet_by', 'sort_by', 'field_limit', 'filter', 'exclude']:
            getattr(mocksolr.query, method).return_value = mocksolr.query
        # set mock facet results via paginator
        mockpage = mockpaginator.return_value.page.return_value
        mock_facets = {
            'object_type': [('audio', 3), ('born-digital', 2)],
            'access_code': [('11', 5)],
            'collection_label': [('My Stuff', 12)],
            'users_facet': [('login1', 22), ('login2', 11)],
            'added_by_facet': [('login2', 12), ('login1', 11)]
        }
        mockpage.object_list.facet_counts.facet_fields = mock_facets
        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # search all
        response = self.client.get(search_url)
        # check solr facet args
        mocksolr.query.facet_by.assert_called_with(KeywordSearch.facet_field_names.values(),
                                                   mincount=1, limit=15, sort='count')
        for solr_field in mock_facets.keys():
            self.assert_(solr_field not in response.context['facets'])

        for display_name, field in KeywordSearch.facet_field_names.iteritems():
            if field in mock_facets:
                self.assert_(display_name in response.context['facets'])

        # search filtered by facet
        response = self.client.get(search_url, {'keyword': 'organs', 'type': 'audio'})
        # query should be filtered by facet value
        mocksolr.query.filter.assert_called_with(object_type='audio')
        # value should not be in list of facets to display
        self.assert_('audio' not in response.context['facets']['type'])
        # value should be displayed with url options to remove filter
        self.assertEqual(('audio', 'keyword=organs'),
                         response.context['active_filters'][0])

        # filters that are ambiguous get massaged labels
        response = self.client.get(search_url, {'added by': 'usr1',
                                                'modified by': 'usr2',
                                                'access status': '10'})
        active_filter_labels = [t for t, u in response.context['active_filters']]
        self.assert_('added by usr1' in active_filter_labels)
        self.assert_('modified by usr2' in active_filter_labels)
        self.assert_('Undetermined' in active_filter_labels)

    def test_search_suggest(self, mocksolr_interface):
        suggest_url = reverse('repo-admin:suggest')
        mocksolr = mocksolr_interface.return_value

        mocksolr.query.return_value = mocksolr.query
        for method in ['query', 'facet_by', 'paginate', 'filter']:
            getattr(mocksolr.query, method).return_value = mocksolr.query

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # empty term - should suggest fields
        response = self.client.get(suggest_url, {'term': ''})
        self.assertEqual('application/json', response['Content-Type'],
             'suggest view should return json content')
        # inspect result
        data = json.loads(response.content)
        # should be based on keyword search form fields
        fields = [i['label'] for i in data]
        self.assertEqual(fields, KeywordSearch.field_descriptions.keys())
        # should have a category set
        for item in data:
            self.assertEqual('Search Fields', item['category'])

        # term ending with space should also suggest fields
        search_term = 'end title:one '
        response = self.client.get(suggest_url, {'term': search_term})
        data = json.loads(response.content)
        self.assert_(data[0]['value'].startswith(search_term),
                     'replacement value should start with existing search term')

        # suggestions for user field
        mocksolr.query.execute.return_value.facet_counts.facet_fields = {
            'users_facet': [
                ('Thing One', 5), ('Thing Two', 4)
            ]
        }
        response = self.client.get(suggest_url, {'term': 'user:'})

        mocksolr.query.facet_by.assert_called_with('users_facet', prefix='',
                                             sort='count', limit=15)
        mocksolr.query.paginate.assert_called_with(rows=0)

        data = json.loads(response.content)
        # inspect results
        self.assertEqual('Thing One (5)', data[0]['label'])
        self.assertEqual('user:"Thing One" ', data[0]['value'])
        self.assertEqual('Users', data[0]['category'])
        self.assertEqual('Thing Two (4)', data[1]['label'])
        self.assertEqual('user:"Thing Two" ', data[1]['value'])
        self.assertEqual('Users', data[1]['category'])

        response = self.client.get(suggest_url, {'term': 'cat user:T'})
        mocksolr.query.facet_by.assert_called_with('users_facet', prefix='T',
                                             sort='count', limit=15)
        data = json.loads(response.content)
        # value should include preceding search string, if any
        self.assertEqual('cat user:"Thing One" ', data[0]['value'])
        self.assertEqual('cat user:"Thing Two" ', data[1]['value'])

        # non-empty but invalid parse result should not error
        response = self.client.get(suggest_url, {'term': ':'})
        self.assertEqual(200, response.status_code)  # was getting a 500 error before fix

    @patch('keep.repoadmin.views.Paginator')
    def test_search_by_created(self, mockpaginator, mocksolr_interface):
        search_url = reverse('repo-admin:search')
        mocksolr = mocksolr_interface.return_value

        mocksolr.query.return_value = mocksolr.query
        for method in ['query', 'facet_by', 'sort_by', 'field_limit', 'filter']:
            getattr(mocksolr.query, method).return_value = mocksolr.query

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # search by user
        self.client.get(search_url, {'keyword': 'created:2012-05'})
        # check solr query args
        # - query should be called with tokenized search terms
        mocksolr.query.query.assert_any_call(created_date='2012-05*')

    def test_search_suggest_created(self, mocksolr_interface):
        suggest_url = reverse('repo-admin:suggest')
        mocksolr = mocksolr_interface.return_value

        mocksolr.query.return_value = mocksolr.query
        for method in ['query', 'facet_by', 'paginate', 'filter']:
            getattr(mocksolr.query, method).return_value = mocksolr.query

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # < 4 digits should query by year
        mocksolr.query.execute.return_value.facet_counts.facet_fields = {
            'created_year': [('2012', 50)]
        }

        response = self.client.get(suggest_url, {'term': 'created:2'})
        mocksolr.query.facet_by.assert_called_with('created_year', prefix='2',
                                             sort='index', limit=15)
        data = json.loads(response.content)
        self.assertEqual('created:2012', data[0]['value'])
        self.assertEqual('Date Added', data[0]['category'])

        # between 4 and 7 digits should query by year-month
        mocksolr.query.execute.return_value.facet_counts.facet_fields = {
            'created_month': [('2012-01', 21)]
        }
        response = self.client.get(suggest_url, {'term': 'created:2012'})
        mocksolr.query.facet_by.assert_called_with('created_month', prefix='2012',
                                             sort='index', limit=15)
        data = json.loads(response.content)
        self.assertEqual('created:2012-01', data[0]['value'])

        # > 7 digits should query by year-month-day
        mocksolr.query.execute.return_value.facet_counts.facet_fields = {
            'created_date': [('2012-01-15', 9)]
        }
        response = self.client.get(suggest_url, {'term': 'created:2012-04'})
        mocksolr.query.facet_by.assert_called_with('created_date', prefix='2012-04',
                                             sort='index', limit=15)
        data = json.loads(response.content)
        self.assertEqual('created:2012-01-15 ', data[0]['value'])


class SearchTemplatesTest(TestCase):

    # define a minimal mock page object to test the template, since
    # django templates don't deal with callable Mock objects well
    class MockPage(object):
        def __init__(self, content=[]):
            self.object_list = content

    search_results = 'repoadmin/results.html'

    # test search result content with one of each type
    content = [
        {'pid': 'audio:1', 'object_type': 'audio', 'title': 'recording'},
        {'pid': 'coll:1', 'object_type': 'collection', 'title': 'mss 123',
         'dsids': ['MODS'], },
        {'pid': 'scoll:1', 'object_type': 'collection', 'title': 'process batch',
         'content_model': SimpleCollection.COLLECTION_CONTENT_MODEL},
        {'pid': 'boda:1', 'object_type': 'born-digital', 'title': 'email'}
    ]

    def setUp(self):
        self.rqst = HttpRequest()

        # basic template context for rendering search results
        form = KeywordSearch({'keyword': 'foo'})
        self.context = {
            'form': form,
            'search_terms': [],
            'search_info': {},
            'show_pages': {},
            'search_opts': {},
            'facets': [],
        }

    def test_results_item_display(self):
        # test search result item display

        # no results
        response = render(self.rqst, self.search_results, self.context)
        self.assertContains(response, 'No matching items found')

        ctx = self.context.copy()
        ctx['page'] = self.MockPage(self.content)
        # use Mock to simulate superuser (any perms check will be non-zero and pass)
        ctx['perms'] = Mock()
        response = render(self.rqst, self.search_results, ctx)

        self.assertContains(response,
                            'sorted by most recently created/uploaded')
        self.assertNotContains(response, 'sorted by relevance')

        self.assertContains(response, reverse('audio:view',
                                              kwargs={'pid': 'audio:1'}),
             msg_prefix='search results should link to view page for audio item')
        self.assertContains(response, reverse('audio:edit',
                                              kwargs={'pid': 'audio:1'}),
             msg_prefix='search results should link to audio edit form for audio item')
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
        for item in self.content:
            self.assertContains(response, item['title'],
                msg_prefix='search results should contain item title "%s"' % \
                                item['title'])

    def test_results_search_terms(self):
        # test template logic for displaying info about current search
        # (terms, field/value terms, sort)

        # unfielded search terms
        ctx = self.context.copy()
        ctx['search_terms'] = ['fantabulous', 'expurgation']
        response = render(self.rqst, self.search_results, ctx)

        self.assertContains(response, 'fantabulous',
            msg_prefix='search term should be displayed on results page')
        self.assertContains(response, 'expurgation',
            msg_prefix='search term should be displayed on results page')

        # sort info
        ctx['show_relevance'] = True
        ctx['page'] = self.MockPage(self.content)
        response = render(self.rqst, self.search_results, ctx)
        self.assertContains(response, 'sorted by relevance')

        # field-based search terms in keyword search string
        ctx['search_info'] = {
            'user': 'admin',
            'added_by': 'one'
        }
        response = render(self.rqst, self.search_results, ctx)
        self.assertContains(response, 'user:',
            msg_prefix='search term field should be displayed on results page')
        self.assertContains(response, 'admin',
            msg_prefix='search term value should be displayed on results page')
        self.assertContains(response, 'sorted by relevance')

        self.assertContains(response, 'added_by:',
            msg_prefix='search term field should be displayed on results page')
        self.assertContains(response, 'one',
            msg_prefix='search term value should be displayed on results page')

        # multiple values for a single field
        ctx['search_info'] = {
            'user': ['bob', 'jane'],
        }
        response = render(self.rqst, self.search_results, ctx)
        self.assertContains(response, 'user:', count=1,
            msg_prefix='search term field should be displayed once on results page')
        self.assertContains(response, 'bob',
            msg_prefix='first search term value should be displayed on results page')
        self.assertContains(response, 'jane',
            msg_prefix='second search term value should be displayed on results page')

    def test_results_facets(self):
        # test template logic for displaying facets

        response = render(self.rqst, self.search_results, self.context)
        self.assertNotContains(response, 'Filter your results')

        mock_facets = {
            'type': [('audio', 3), ('born-digital', 2)],
            'access status': [('11', 5)],
            'collection': [('My Stuff', 15)],
            'modified by': [('login1', 32), ('login2', 31)],
            'added by': [('login2', 12), ('login1', 10)]
        }
        ctx = self.context.copy()
        ctx['facets'] = mock_facets
        ctx['url_params'] = 'keyword=interesting stuff'
        response = render(self.rqst, self.search_results, ctx)
        self.assertContains(response, 'Filter your results')

        for field in mock_facets.iterkeys():
            self.assertContains(response, field,
                msg_prefix='facet field name should be listed')

            for term, count in mock_facets[field]:
                # term should be listed as link text
                if field == 'access status':
                    self.assertContains(response, '>Unknown from Old DM<',
                        msg_prefix='for access status, abbreviation should be listed')
                else:
                    self.assertContains(response, '>%s<' % term,
                        msg_prefix='facet value should be listed')

                self.assertContains(response, '(%s)' % count,
                    msg_prefix='facet count should be listed')
                self.assertContains(response, '?%s&amp;%s=%s' % (ctx['url_params'],
                                                                 field, term),
                    msg_prefix='page should include link to search + facet value')
