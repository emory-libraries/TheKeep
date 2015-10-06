from contextlib import contextmanager
import json
import logging
from mock import Mock, patch, NonCallableMock
from os import path
from django.contrib.auth import get_user_model
from rdflib import URIRef
from rdflib.namespace import RDF
from sunburnt import sunburnt

from django.conf import settings
from django.core.urlresolvers import reverse, resolve
from django.test import Client
from django.utils.http import urlquote

from eulfedora.rdfns import relsext
from eulfedora.util import RequestFailed
from eulxml.xmlmap import mods
from eulcm.xmlmap.mods import MODS

from keep.audio.models import AudioObject
from keep.accounts.models import ResearcherIP
from keep.arrangement.models import ArrangementObject
from keep.collection.fixtures import FedoraFixtures
from keep.collection import forms as cforms
from keep.collection import views
from keep.collection.models import CollectionObject, FindingAid, SimpleCollection
from keep.collection.views import _objects_by_type
from keep.collection.tasks import batch_set_status
from keep.common.fedora import DigitalObject, Repository
from keep.common.rdfns import REPO
from keep.testutil import KeepTestCase

logger = logging.getLogger(__name__)

# NOTE: this user must be defined as a fedora user for certain tests to work
ADMIN_CREDENTIALS = {'username': 'euterpe', 'password': 'digitaldelight'}


class CollectionObjectTest(KeepTestCase):
    # tests for Collection DigitalObject

    def setUp(self):
        super(CollectionObjectTest, self).setUp()
        # get rid of any pre-cached archives
        CollectionObject._archives = None

    def tearDown(self):
        super(CollectionObjectTest, self).tearDown()
        # remove any archives cached by the tests
        CollectionObject._archives = None

    @patch('keep.collection.models.solr_interface')
    def test_archives(self, mock_solr_interface):
        # NOTE: mock order/syntax depends on how it is used in the method
        solrquery = mock_solr_interface.return_value.query
        solr_exec = solrquery.return_value.exclude.return_value.sort_by.return_value.execute

        solr_exec.return_value = [
            {'pid': 'coll:1', 'label': 'marbl'},
            {'pid': 'coll:2', 'label': 'eua'},
            {'pid': 'coll:3', 'label': 'pitts'},
        ]
        collections = CollectionObject.archives()
        found_pids = [obj.pid for obj in collections]
        for pid in [coll['pid'] for coll in solr_exec.return_value]:
            self.assert_(pid in found_pids,
                         'pid %s from mock solr return should be in returned objects' % pid)

        self.assertEqual(len(solr_exec.return_value), len(collections),
             "number of items returned should match solr result")
        self.assert_(isinstance(collections[0], CollectionObject),
                "top-level collection is instance of CollectionObject")
        args, kwargs = solrquery.call_args
        self.assertEqual(CollectionObject.COLLECTION_CONTENT_MODEL, kwargs['content_model'],
                         'solr query should filter on collection object content model')
        args, kwargs = solrquery.return_value.exclude.call_args
        self.assertEqual(True, kwargs['archive_id__any'],
                     'solr query should exclude results with any collection id to find top-level collections')

    def test_creation(self):
        obj = self.repo.get_object(type=CollectionObject)
        self.assertEqual(settings.FEDORA_OBJECT_OWNERID, obj.info.owner)

    def test_update_dc(self):
        # DC should get updated from MODS & RELS-EXT on save

        # create test object and populate with data
        obj = self.repo.get_object(type=CollectionObject)
        # collection membership in RELS-EXT
        collections = FedoraFixtures.archives()
        obj.collection = self.repo.get_object(collections[0].uri)
        obj.mods.content.source_id = '1000'
        obj.mods.content.title = 'Salman Rushdie Papers'
        obj.mods.content.resource_type = 'mixed material'
        # name
        obj.mods.content.create_name()
        obj.mods.content.name.name_parts.append(mods.NamePart(text='Salman Rushdie'))
        obj.mods.content.name.roles.append(mods.Role(text='author', authority='local'))
        # date range
        obj.mods.content.create_origin_info()
        obj.mods.content.origin_info.created.append(mods.DateCreated(date=1947, point='start'))
        obj.mods.content.origin_info.created.append(mods.DateCreated(date=2008, point='end'))

        # update DC and check values
        obj._update_dc()
        self.assert_('1000' in obj.dc.content.identifier_list,
            'source identifier should be present in a dc:identifier')
        self.assertEqual(obj.mods.content.title, obj.dc.content.title,
            'dc:title should match title from MODS')
        self.assertEqual(obj.mods.content.resource_type, obj.dc.content.type,
            'dc:type should match resource type from MODS')
        self.assertEqual('Salman Rushdie', obj.dc.content.creator,
            'dc:creator set from MODS name')
        self.assertEqual('1947-2008', obj.dc.content.date,
            'dc:date has text version of date range from MODS')

        # change values - test updated in DC correctly
        obj.mods.content.source_id = '123'
        obj.mods.content.title = 'Thomas Esterbrook letter books'
        obj.mods.content.resource_type = 'text'
        # name
        obj.mods.content.name.name_parts[0].text = 'Thomas Esterbrook'
        # single date
        obj.mods.content.origin_info.created.pop()  # remove second date
        obj.mods.content.origin_info.created[0].date = 1950
        obj.mods.content.origin_info.created[0].point = None

        obj._update_dc()
        self.assert_('123' in obj.dc.content.identifier_list,
            'updated source identifier should be present in a dc:identifier')
        self.assert_('1000' not in obj.dc.content.identifier_list,
            'previous source identifier should not be present in a dc:identifier')
        self.assertEqual(obj.mods.content.title, obj.dc.content.title,
            'dc:title should match updated title from MODS')
        self.assertEqual(obj.mods.content.resource_type, obj.dc.content.type,
            'dc:type should match updated resource type from MODS')
        self.assertEqual('Thomas Esterbrook', obj.dc.content.creator,
            'dc:creator set from updated MODS name')
        self.assertEqual('1950', obj.dc.content.date,
            'dc:date has single date from MODS')

    @contextmanager
    def ingest_test_collections(self):
        self.rushdie = FedoraFixtures.rushdie_collection()
        self.rushdie.save()
        self.esterbrook = FedoraFixtures.esterbrook_collection()
        self.esterbrook.save()
        self.engdocs = FedoraFixtures.englishdocs_collection()
        self.engdocs.save()

        pids = [self.rushdie.pid, self.esterbrook.pid, self.engdocs.pid]
        yield pids

        for p in pids:
            self.repo.purge_object(p)
        self.rushdie = None
        self.esterbrook = None
        self.engdocs = None

    # set up a mock solr object for use in solr-based find methods
    mocksolr = Mock(sunburnt.SolrInterface)
    mocksolr.return_value = mocksolr
    # solr interface has a fluent interface where queries and filters
    # return another solr query object; simulate that as simply as possible
    mocksolr.query.return_value = mocksolr.query
    mocksolr.query.query.return_value = mocksolr.query
    mocksolr.query.paginate.return_value = mocksolr.query
    mocksolr.query.exclude.return_value = mocksolr.query

    @patch('keep.collection.models.solr_interface', mocksolr)
    def test_item_collections(self):
        solr_result = [
            {'pid': 'coll:1', 'label': 'foo'},
            {'pid': 'coll:2', 'label': 'bar'},
            {'pid': 'coll:3', 'label': 'baz'},
        ]
        self.mocksolr.query.execute.return_value = solr_result

        collections = CollectionObject.item_collections()
        # returns a list of dict ~= solr result
        self.assertEqual(solr_result, collections,
             "item_collections method should return solr results")
        args, kwargs = self.mocksolr.query.call_args
        self.assertEqual(CollectionObject.COLLECTION_CONTENT_MODEL, kwargs['content_model'],
                         'solr query should filter on collection object content model')
        self.assertEqual(True, kwargs['archive_id__any'],
                         'solr query should include objects with any parent collection id')

    @patch('keep.collection.models.solr_interface', mocksolr)
    def test_subcollections(self):
        solr_result = [
            {'pid': 'coll:1', 'label': 'foo'},
            {'pid': 'coll:2', 'label': 'bar'},
            {'pid': 'coll:3', 'label': 'baz'},
        ]
        self.mocksolr.query.execute.return_value = solr_result

        marbl = CollectionObject(api=Mock())
        marbl.pid = 'coll:marbl'
        subcolls = marbl.subcollections()
        # returns a list of dict ~= solr result
        self.assertEqual(solr_result, subcolls,
             "subcollections method should return solr results")

        # inspect solr query args
        args, kwargs = self.mocksolr.query.call_args
        self.assertEqual(CollectionObject.COLLECTION_CONTENT_MODEL, kwargs['content_model'],
                         'solr query should filter on collection object content model')
        self.assertEqual('%s:' % settings.FEDORA_PIDSPACE, kwargs['pid'],
                         'solr query should filter on configured pidspace')
        self.assertEqual(marbl.pid, kwargs['archive_id'],
                         'solr query should filter on collection pid of current object')

    @patch('keep.collection.models.solr_interface', mocksolr)
    def test_find_by_collection_number(self):
        # sample result to be returned
        result = [
            {'pid': 'coll:1', 'label': 'foo', 'source_id': 1000},
        ]
        self.mocksolr.query.execute.return_value = result

        # search by number only
        search_coll = 1000
        found = list(CollectionObject.find_by_collection_number(search_coll))
        self.assertEqual(result[0]['pid'], found[0].pid)
        self.assert_(isinstance(found[0], CollectionObject),
                     'results should be returned as instance of CollectionObject')
        args, kwargs = self.mocksolr.query.call_args
        self.assertEqual(search_coll, kwargs['source_id'],
                         'solr query should search for requested collection number in source_id')
        self.assertEqual('%s:*' % settings.FEDORA_PIDSPACE, kwargs['pid'],
                         'solr query should filter on configured pidspace')
        self.assertEqual(CollectionObject.COLLECTION_CONTENT_MODEL, kwargs['content_model'],
                         'solr query should filter on collection content model')
        # test pagination?

        # search by number and parent collection
        search_coll = 1000
        parent_collection = 'parent:1'
        found = list(CollectionObject.find_by_collection_number(search_coll, parent_collection))
        self.assertEqual(result[0]['pid'], found[0].pid)
        args, kwargs = self.mocksolr.query.call_args
        self.assertEqual(search_coll, kwargs['source_id'],
            'find by mss number with parent option should still search for requested collection number in source_id')
        # subquery - optional filter when parent is specified
        args, kwargs = self.mocksolr.query.query.call_args
        self.assertEqual(parent_collection, kwargs['archive_id'],
            'find by mss number with parent option should filter on archive_id')

        # empty result
        self.mocksolr.query.execute.return_value = []
        found = list(CollectionObject.find_by_collection_number(search_coll, parent_collection))
        self.assertEqual([], found,
            'when solr returns no results, find by collection number returns an empty list')

    def test_index_data_descriptive(self):
        # test descriptive metadata used for indexing objects in solr

        # use a mock object to simulate pulling archive object from Fedora
        mockarchive = Mock(CollectionObject)
        mockarchive.pid = 'parent:1'
        mockarchive.uri = 'info:fedora/parent:1'
        mockarchive.label = 'Manuscript, Archive, and Rare Book Library'
        mockarchive.mods.content.short_name = 'MARBL'

        # create test object and populate with data
        obj = self.repo.get_object(type=CollectionObject)
        obj.dc.content.title = 'test collection'

        # test index data for parent archive separately
        # NOTE: collection is a descriptor so must be patched on the *class*
        # instead of the object
        with patch('keep.collection.models.CollectionObject.collection',
                   mockarchive):
            arch_data = obj._index_data_archive()
            self.assertEqual(obj.collection.pid, arch_data['archive_id'],
                'parent collection object (archive) id should be set in index data')
            self.assertEqual(mockarchive.label, arch_data['archive_label'],
                'parent collection object (archive) label should be set in index data')
            self.assertEqual(mockarchive.mods.content.short_name, arch_data['archive_short_name'],
                'parent collection object (archive) short name should be set in index data')
            # error if data is not serializable as json
            self.assert_(json.dumps(arch_data))

        # skip index archive data and test the rest
        with patch.object(obj, '_index_data_archive', Mock(return_value={})):
            desc_data = obj.index_data_descriptive()
            self.assert_('source_id' not in desc_data,
                         'source_id should not be included in index data when it is not set')
            self.assertEqual(obj.dc.content.title, desc_data['title'][0],
                             'default index data fields should be present in data')

            obj.mods.content.source_id = 100
            desc_data = obj.index_data_descriptive()
            self.assertEqual(obj.mods.content.source_id, desc_data['source_id'],
                             'source id should be included in index data when set')
            # error if data is not serializable as json
            self.assert_(json.dumps(desc_data))


# sample POST data for creating a collection
COLLECTION_DATA = {
    'title': 'Rushdie papers',
    'source_id': '1000',
    'date_created': '1947',
    'date_end': '2008',
    'collection': 'emory:93z53',
    'resource_type': 'mixed material',
    'use_and_reproduction-text': 'no photos',
    'restrictions_on_access-text': 'tuesdays only',
    'name-type': 'personal',
    'name-authority': 'local',
    # 'management' form data is required for django to process formsets
    'name-name_parts-INITIAL_FORMS': '0',
    'name-name_parts-TOTAL_FORMS': '1',
    'name-name_parts-MAX_NUM_FORMS': '',
    'name-name_parts-0-text': 'Mr. So and So',
    'name-roles-TOTAL_FORMS': '1',
    'name-roles-INITIAL_FORMS': '0',
    'name-roles-MAX_NUM_FORMS': '',
    'name-roles-0-authority': 'local',
    'name-roles-0-type': 'text',
    'name-roles-0-text': 'curator',
}


# mock archives used to generate archives choices for form field
@patch('keep.collection.forms.CollectionObject.archives',
       new=Mock(return_value=FedoraFixtures.archives(format=dict)))
class TestCollectionForm(KeepTestCase):
    # test form data with all required fields
    data = COLLECTION_DATA

    def setUp(self):
        super(TestCollectionForm, self).setUp()
        self.form = cforms.CollectionForm(self.data)
        self.obj = FedoraFixtures.rushdie_collection()
        self.archives = FedoraFixtures.archives()
        # store initial collection object from fixture
        self.collection = self.obj.collection

    def test_subform_classes(self):
        # test that subforms are initialized with the correct classes
        sub = self.form.subforms['restrictions_on_access']
        self.assert_(isinstance(sub, cforms.AccessConditionForm),
                    "restrictions on access subform should be instance of AccessConditionForm, got %s" \
                    % sub.__class__)
        sub = self.form.subforms['use_and_reproduction']
        self.assert_(isinstance(sub, cforms.AccessConditionForm),
                    "use & reproduction subform should be instance of AccessConditionForm, got %s" \
                    % sub.__class__)
        sub = self.form.subforms['name']
        self.assert_(isinstance(sub, cforms.NameForm),
                    "name subform should be instance of NameForm, got %s" % sub.__class__)
        fs = self.form.subforms['name'].formsets['name_parts'].forms[0]
        self.assert_(isinstance(fs, cforms.NamePartForm),
                    "name_parts form should be instance of NamePartForm, got %s" % \
                    fs.__class__)

    @patch('keep.collection.forms.solr_interface')
    def test_update_instance(self, mock_solr_interface):
        # test custom save logic for date created

        # configure solr response for form validation
        solr_response = mock_solr_interface.return_value.query.return_value \
                            .execute.return_value
        solr_response.result.numFound = 0

        # - must be valid to update instance
        self.assertTrue(self.form.is_valid(), "test form object with test data is valid")
        # initial data has start and end date
        mods = self.form.update_instance()
        expected, got = 2, len(mods.origin_info.created)
        self.assertEqual(expected, got,
            "expected %d created dates when date range is submitted, got %d" % \
            (expected, got))
        self.assertEqual(self.data['date_created'], mods.origin_info.created[0].date)
        self.assertEqual('start', mods.origin_info.created[0].point,
            'first date should have point=start when date range is submitted')
        self.assertTrue(mods.origin_info.created[0].key_date,
            'first created date should have key_date = True')
        self.assertEqual(self.data['date_end'], mods.origin_info.created[1].date)
        self.assertEqual('end', mods.origin_info.created[1].point,
            'second date should have point=end when date range is submitted')

        # start date only (not a date range)
        data = self.data.copy()
        del(data['date_end'])
        form = cforms.CollectionForm(data)
        self.assertTrue(form.is_valid(), "test form object with test data is valid")
        mods = form.update_instance()
        expected, got = 1, len(mods.origin_info.created)
        self.assertEqual(expected, got,
            "expected %d created dates when single created date is submitted, got %d" % \
            (expected, got))
        self.assertEqual(self.data['date_created'], mods.origin_info.created[0].date)
        self.assertEqual(None, mods.origin_info.created[0].point,
            "created date should have no point attribute when single date is submitted")
        self.assertTrue(mods.origin_info.created[0].key_date)

        # change collection and confirm set in RELS-EXT
        data = self.data.copy()
        data['collection'] = self.archives[2].pid
        form = cforms.CollectionForm(data, instance=self.obj)
        self.assertTrue(form.is_valid(), "test form object with test data is valid")
        form.update_instance()
        self.assertEqual(self.archives[2].pid, self.obj.collection.pid)

    def test_initial_data(self):
        form = cforms.CollectionForm(instance=self.obj)
        # custom fields that are not handled by XmlObjectForm have special logic
        # to ensure they get set when an instance is passed in
        expected, got = self.collection.pid, form.initial['collection']
        self.assertEqual(expected, got,
            'collection pid is set correctly in form initial data from instance; expected %s, got %s' \
            % (expected, got))
        expected, got = '1947', form.initial['date_created']
        self.assertEqual(expected, got,
            'date created is set correctly in form initial data from instance; expected %s, got %s' \
            % (expected, got))
        expected, got = '2008', form.initial['date_end']
        self.assertEqual(expected, got,
            'date end is set correctly in form initial data from instance; expected %s, got %s' \
            % (expected, got))


# mock archives used to generate archives choices for form field
@patch('keep.collection.forms.CollectionObject.archives',
       new=Mock(return_value=FedoraFixtures.archives(format=dict)))
class CollectionViewsTest(KeepTestCase):
    fixtures = ['users', 'initial_groups']
    # default groups must be loaded for group-based permissions

    def setUp(self):
        super(CollectionViewsTest, self).setUp()
        self.client = Client()
        self.pids = []

    def tearDown(self):
        super(CollectionViewsTest, self).tearDown()
        # purge any objects created by individual tests
        for pid in self.pids:
            try:
                self.repo.purge_object(pid)
            except RequestFailed:
                logger.warn('Failed to purge %s in tear down' % pid)

    @patch('keep.collection.forms.solr_interface')
    def test_create(self, mock_solr_interface):
        # test creating a collection object

        # configure solr response for form validation
        solr_response = mock_solr_interface.return_value.query.return_value \
                            .execute.return_value
        solr_response.result.numFound = 0

        # log in as staff
        # NOTE: using admin view so user credentials will be used to access fedora
        self.client.post(settings.LOGIN_URL, ADMIN_CREDENTIALS)

        new_coll_url = reverse('collection:new')

        response = self.client.get(new_coll_url)
        expected, code = 200, response.status_code
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, new_coll_url))
        self.assert_(isinstance(response.context['form'], cforms.CollectionForm),
                "MODS CollectionForm is set in response context")

        # test submitting incomplete/invalid data - should redisplay form with errors
        bad_data = COLLECTION_DATA.copy()
        del(bad_data['source_id'])
        del(bad_data['resource_type'])
        bad_data['collection'] = 'bogus-pid:123'
        response = self.client.post(new_coll_url, bad_data)
        self.assert_(isinstance(response.context['form'], cforms.CollectionForm),
                "MODS CollectionForm is set in response context after invalid submission")
        self.assertContains(response, 'This field is required', 2,
            msg_prefix='error message for 2 missing required fields')
        self.assertContains(response, 'Select a valid choice',
            msg_prefix='error message for collection pid not in list')

        # submit a duplicate collection - should redisplay with errors
        data = COLLECTION_DATA.copy()
        solr_response.result.numFound = 1
        solr_response[0]['pid'] = 'pidspace:otherpid'
        response = self.client.post(new_coll_url, data)
        self.assert_(isinstance(response.context['form'], cforms.CollectionForm),
                "MODS CollectionForm is set in response context after duplicate submission")
        self.assertContains(response, 'A collection already exists with this Archive and Source Id', 2,
            msg_prefix='error message for duplicate archive/source id')

        # POST and create new object, verify in fedora
        data = COLLECTION_DATA.copy()
        data['_save_continue'] = True   # use 'save and continue' so we can get created object from response
        solr_response.result.numFound = 0
        response = self.client.post(new_coll_url, data, follow=True)
        # do we need to test actual response, redirect ?
        messages = [str(msg) for msg in response.context['messages']]
        self.assert_('Successfully created collection' in messages[0],
            'successful collection creation message displayed to user')
        # inspect newly created object and in fedora

        repo = Repository()
        new_coll = repo.get_object(response.context['collection'].pid, type=CollectionObject)
        # check object creation and init-specific logic handled by view (isMemberOf)
        self.assertTrue(new_coll.has_model(CollectionObject.COLLECTION_CONTENT_MODEL),
            "collection object was created with the correct content model")
        self.assertEqual(COLLECTION_DATA['title'], new_coll.mods.content.title,
            "MODS content created on new object from form data")
        # collection membership
        self.assert_((URIRef(new_coll.uri),
                      relsext.isMemberOfCollection,
                      URIRef('info:fedora/%s' % COLLECTION_DATA['collection'])) in
                      new_coll.rels_ext.content,
                      "collection object is member of requested top-level collection")

        # confirm that current site user appears in fedora audit trail
        xml = new_coll.api.getObjectXML(new_coll.pid).content
        self.assert_('<audit:responsibility>%s</audit:responsibility>' % ADMIN_CREDENTIALS['username'] in xml)

#    @patch('keep.search.views.solr_interface')  # site-index on redirect - do we need this too?
    @patch('keep.collection.forms.solr_interface')
    def test_edit(self, mock_solr_interface):
        # configure solr response for form validation
        solr_response = mock_solr_interface.return_value.query.return_value \
                            .execute.return_value
        solr_response.result.numFound = 0

        repo = Repository()
        obj = FedoraFixtures.rushdie_collection()
        # store initial collection id from fixture
        collection_pid = obj.collection.pid
        obj.save()  # save to fedora for editing
        self.pids.append(obj.pid)

        # log in as staff
        # NOTE: using admin view so user credentials will be used to access fedora
        self.client.post(settings.LOGIN_URL, ADMIN_CREDENTIALS)
        edit_url = reverse('collection:edit', args=[obj.pid])

        response = self.client.get(edit_url)
        expected, code = 200, response.status_code
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, edit_url))
        self.assert_(isinstance(response.context['form'], cforms.CollectionForm),
                "MODS CollectionForm is set in response context")
        self.assert_(isinstance(response.context['form'].instance, MODS),
                "form instance is a collection MODS XmlObject")
        self.assertContains(response, 'value="1000"',
                msg_prefix='MSS # from existing object set as input value')
        self.assertContains(response, 'value="Salman Rushdie Collection"',
                msg_prefix='Title from existing object set as input value')
        self.assertContains(response, 'value="1947"',
                msg_prefix='Start date from existing object set as input value')
        self.assertContains(response, 'value="2008"',
                msg_prefix='End date from existing object set as input value')
        self.assertContains(response, 'value="%s" selected="selected"' % collection_pid,
                msg_prefix='Parent collection from existing object pre-selected')
        self.assertContains(response, 'Edit Collection',
                msg_prefix='page title indicates user is editing an existing collection')
        self.assertContains(response, 'name="name-name_parts-0-DELETE"',
                msg_prefix='namePart delete option is available for first name part')
        self.assertNotContains(response, 'name="name-name_parts-1-DELETE"',
                msg_prefix='namePart delete option is not available for extra name part')
        self.assertNotContains(response, 'name="name-roles-0-DELETE"',
                msg_prefix='name role delete option is not available (no initial role data)')

        # POST and update existing object, verify in fedora
        response = self.client.post(edit_url, COLLECTION_DATA, follow=True)
        messages = [str(msg) for msg in response.context['messages']]
        self.assert_(messages[0].startswith('Successfully updated collection'),
            'successful collection update message displayed to user')
        self.assert_(obj.pid in messages[0],
            'success message includes object pid')
        obj = repo.get_object(type=CollectionObject, pid=obj.pid)
        self.assertEqual(COLLECTION_DATA['title'], obj.mods.content.title,
            "MODS content updated in existing object from form data")
        # confirm that current site user appears in fedora audit trail
        xml = obj.api.getObjectXML(obj.pid).content
        self.assert_('<audit:responsibility>%s</audit:responsibility>' % ADMIN_CREDENTIALS['username'] in xml,
            'user logged into site is also username in fedora audit:trail')

        #test audit trail
        obj = repo.get_object(pid=obj.pid, type=CollectionObject)
        audit_trail = [a.message for a in obj.audit_trail.records]
        self.assertEqual('updating metadata', audit_trail[-1])

        #test with comment
        data = COLLECTION_DATA.copy()
        data['comment'] = 'This is a comment'
        data['date_end'] = '2000'  # change something to trigger save
        response = self.client.post(edit_url, data, follow=True)
        obj = repo.get_object(pid=obj.pid, type=CollectionObject)
        audit_trail = [a.message for a in obj.audit_trail.records]
        self.assertEqual(data['comment'], audit_trail[-1])

        # test logic for save and continue editing
        data = COLLECTION_DATA.copy()
        data['_save_continue'] = True   # simulate submit via 'save and continue' button
        response = self.client.post(edit_url, data)
        messages = [str(msg) for msg in response.context['messages']]
        self.assert_(messages[0].startswith('Successfully updated collection'),
            'successful collection update message displayed to user on save and continue editing')
        self.assert_(isinstance(response.context['form'], cforms.CollectionForm),
                "MODS CollectionForm is set in response context after save and continue editing")

        # validation errors - post incomplete/bogus data & check for validation errors
        data = COLLECTION_DATA.copy()
        data.update({
            'title': '',       # title is required
        })
        response = self.client.post(edit_url, data)
        messages = [str(msg) for msg in response.context['messages']]
        self.assert_(messages[0].startswith("Your changes were not saved due to a validation error"),
            "form validation error message set in response context")

        # save & continue when creating a new record
        new_collection_url = reverse('collection:new')
        data = COLLECTION_DATA.copy()
        data['_save_continue'] = True   # simulate submit via 'save and continue' button
        # for a new collection, should redirect to edit collection url (with pid)
        response = self.client.post(new_collection_url, data, follow=True)
        redirect_url, redirect_code = response.redirect_chain[0]
        self.assertEqual(303, redirect_code,
            'save and continue editing on new collection should redirect with 303, got %s' \
            % redirect_code)
        # resolve the redirect url and confirm it redirected to edit-collection
        # - redirect url is absolute, strip off django testserver hostname for resolvable path
        redirect_url = redirect_url[len('http://testserver'):]
        view_func, args, kwargs = resolve(redirect_url)
        # set the newly created object to be cleaned up after tests complete
        self.pids.append(kwargs['pid'])
        self.assertEqual(views.edit, view_func,
            'redirect url %s should resolve to edit_collection view' % redirect_url)
        self.assert_('pid' in kwargs, 'object pid is set in resolved url keyword args')

        messages = [str(msg) for msg in response.context['messages']]
        self.assert_('Successfully created collection' in messages[0],
            'successful collection creation message displayed to user on save and continue editing')

        # editing source id/archive to create a duplicate should fail.
        data = COLLECTION_DATA.copy()
        solr_response.result.numFound = 1
        solr_response[0]['pid'] = 'pidspace:otherpid'
        response = self.client.post(new_collection_url, data, follow=True)
        self.assert_(isinstance(response.context['form'], cforms.CollectionForm),
                "MODS CollectionForm is set in response context after duplicate submission")
        self.assertContains(response, 'A collection already exists with this Archive and Source Id', 2,
            msg_prefix='error message for duplicate archive/source id')

        # attempt to edit non-existent record
        edit_url = reverse('collection:edit', args=['my-bogus-pid:123'])
        response = self.client.get(edit_url)
        expected, code = 404, response.status_code
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s (non-existing pid)'
                             % (expected, code, edit_url))

    @patch('keep.collection.views.solr_interface')
    def test_search(self, mock_solr_interface):
        search_url = reverse('collection:search')

        # using a mock for sunburnt so we can inspect method calls,
        # simulate search results, etc.

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # unused ?!
        # default_search_args = {
        #     'pid': '%s:*' % settings.FEDORA_PIDSPACE,
        #     'content_model': CollectionObject.COLLECTION_CONTENT_MODEL,
        # }

        # search all collections (no user-entered search terms)
        response = self.client.get(search_url)
        args, kwargs = mock_solr_interface.return_value.query.call_args
        # default search args that should be included on every collection search
        self.assertEqual(CollectionObject.COLLECTION_CONTENT_MODEL, kwargs['content_model'],
                         'collection search should be filtered by collection content model')
        self.assertEqual('%s:*' % settings.FEDORA_PIDSPACE, kwargs['pid'],
                         'collection search should be filtered by configured pidspace')

        # search by MSS # (AKA source id)
        mss = 1000
        response = self.client.get(search_url, {'collection-source_id': mss})
        args, kwargs = mock_solr_interface.return_value.query.call_args
        self.assertEqual(mss, kwargs['source_id'],
                         'source id number should be included in solr query terms')
        self.assert_('title' not in kwargs,
                     'title should not be in solr query args when no title terms entered')
        self.assert_('creator' not in kwargs,
                     'creator should not be in solr query args when no creator terms entered')
        self.assert_('archive_id' not in kwargs,
                     'archive_id should not be in solr query args when no collection was selected')
        self.assertEqual(mss, response.context['search_info']['Collection Number'],
                         'source id should be included in search info for user display as collection number')

        # search by title
        search_title = 'collection'
        response = self.client.get(search_url, {'collection-title': search_title})
        args, kwargs = mock_solr_interface.return_value.query.call_args
        self.assertEqual(search_title, kwargs['title'],
                         'title search term should be included in solr query terms')
        self.assert_('source_id' not in kwargs)
        self.assertEqual(search_title, response.context['search_info']['title'],
                         'title search term should be included in search info for display to user')

        # search by creator
        creator = 'esterbrook'
        response = self.client.get(search_url, {'collection-creator': creator})
        args, kwargs = mock_solr_interface.return_value.query.call_args
        self.assertEqual(creator, kwargs['creator'],
                         'creator search term should be included in solr query terms')
        self.assertEqual(creator, response.context['search_info']['creator'],
                         'creator search term should be included in search info for display to user')

        # search by numbering scheme
        collection = FedoraFixtures.archives()[1]
        with patch('keep.collection.models.CollectionObject.find_by_pid',
                   new=Mock(return_value={'title': collection.label, 'pid': collection.pid})):
            response = self.client.get(search_url, {'collection-archive_id': collection.pid})
            args, kwargs = mock_solr_interface.return_value.query.call_args
            self.assertEqual(collection.pid, kwargs['archive_id'],
                'selected archive_id should be included in solr query terms')
            self.assertEqual(collection.pid, response.context['search_info']['Archive']['pid'],
                'archive label should be included in search info for display to user')

        # shortcut to set the solr return value
        # NOTE: call order here has to match the way methods are called in view
        solrquery = mock_solr_interface.return_value.query.return_value.sort_by.return_value
        solr_exec = solrquery.paginate.return_value.execute

        # no match
        # - set mock solr to return an empty result list
        solr_exec.return_value = []
        response = self.client.get(search_url, {'collection-title': 'not-a-collection'})
        self.assertContains(response, 'no results',
                msg_prefix='Message should be displayed to user when search finds no matches')

        # when a result has  no title, default text should be displayed
        # sunburnt solr queries return a list of dictionaries; return one with an empty title
        solr_exec.return_value = [
            {'pid': 'foo', 'creator': 'so and so', 'title': ''}
        ]
        response = self.client.get(search_url,)
        self.assertContains(response, '(no title present)',
            msg_prefix='when a collection has no title, default no-title text is displayed')

    @patch('keep.collection.views.solr_interface')
    @patch('keep.collection.views.CollectionObject')
    def test_list_archives(self, mockcollobj, mocksolr_interface):
        archive_url = reverse('collection:list-archives')

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # setup solr mock
        mocksolr = mocksolr_interface.return_value
        mocksolr.query.return_value = mocksolr.query
        for method in ['query', 'field_limit', 'sort_by']:
            getattr(mocksolr.query, method).return_value = mocksolr.query

        solr_result = [
            {'pid': settings.PID_ALIASES['marbl'],
             'title': 'Manuscript, Archive, and Rare Book Library'},
             {'pid': settings.PID_ALIASES['eua'],
             'title': 'Emory University Archives'},
        ]
        mocksolr.query.__iter__.return_value = solr_result

        # setup mock collection solr query
        mockcollq = mockcollobj.item_collection_query.return_value
        for method in ['query', 'facet_by', 'paginate', 'filter', 'join']:
            getattr(mockcollq, method).return_value = mockcollq

        # mock facets for collection counts
        mockcollq.execute.return_value.facet_counts.facet_fields = {
            'archive_id': [
                (settings.PID_ALIASES['marbl'], 37),
                (settings.PID_ALIASES['eua'], 1),
            ]
        }
        response = self.client.get(archive_url)
        # inspect display
        # - titles should be displayed
        self.assertContains(response, solr_result[0]['title'],
            msg_prefix='page should display archive label')
        self.assertContains(response, solr_result[1]['title'],
            msg_prefix='page should display archive label')
        # - should link to archive browse page
        self.assertContains(response, reverse('collection:browse-archive',
            kwargs={'archive': 'marbl'}),
            msg_prefix='should link to archive browse page for marbl')
        self.assertContains(response, reverse('collection:browse-archive',
            kwargs={'archive': 'eua'}),
            msg_prefix='should link to archive browse page for eua')
        # - should display number of collectiosn based on facet
        self.assertContains(response, '37 collections',
            msg_prefix='should display number of collections for marbl')
        self.assertContains(response, '1 collection',
            msg_prefix='should display number of collections for eua')

        # logout to test guest/researcher access
        self.client.logout()
        response = self.client.get(archive_url)
        expected, got = 302, response.status_code
        self.assertEqual(expected, got,
            'Expected status code %s when accessing %s as guest, got %s' % \
            (expected, got, archive_url))
        self.assert_(reverse('accounts:login') in response['Location'],
            'guest access to search should redirect to login page')

        # create researcher IP for localhost so anonymous access will be
        # treated as anonymous researcher
        researchip = ResearcherIP(name='test client', ip_address='127.0.0.1')
        researchip.save()
        response = self.client.get(archive_url)
        # check that join query for researcher perms was called
        mockcollq.join.assert_any_call('collection_id', 'pid', researcher_access=True)
        mockcollq.join.assert_any_call('collection_id', 'pid', has_access_copy=True)
        researchip.delete()

    @patch('keep.collection.views.solr_interface')
    @patch('keep.collection.views.CollectionObject')
    @patch.object(cforms.FindCollection, 'archive_choices_by_user')
    def test_find_collection(self, mockarch_choices, mockcollobj, mocksolr_interface):
        # test shortcut method to find a collection
        archive_url = reverse('collection:list-archives')

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # setup mock collection solr query
        mockcollq = mockcollobj.item_collection_query.return_value
        for method in ['query', 'facet_by', 'paginate']:
            getattr(mockcollq, method).return_value = mockcollq
        # mimic single result found
        mockcollq.count.return_value = 1
        solr_result = [
            {'pid': 'test:1'},
        ]
        mockcollq.__getitem__.return_value = solr_result[0]

        # patch archive_choices_by_user so search input will be valid
        mockarch_choices.return_value = [('marbl', 'MARBL')]

        # search by archive & id
        coll_data = {'archive': 'marbl', 'collection': '1000'}
        response = self.client.get(archive_url, coll_data)

        self.assert_(response['Location'].endswith(reverse('collection:view',
                     kwargs={'pid': solr_result[0]['pid']})),
            'should redirect to collection view when one result is found')
        self.assertEqual(303, response.status_code,
            'find collection should redirect with 303 when 1 match is found, got %s' \
            % response.status_code)

        # retrieve index page to test messages set
        # NOTE: this is simpler than following the redirect (would require additional mocks)
        response = self.client.get(reverse('site-index'))
        msg = list(response.context['messages'])[0]
        self.assertEqual('One collection found for MARBL 1000.', str(msg),
            'user should see message indicating one collection was found')
        self.assertEqual('info', msg.tags,
            'message should be of type info')

        # mimic multiple results found
        mockcollq.count.return_value = 3
        # search by archive & id
        coll_data = {'archive': 'marbl', 'collection': '1000'}
        response = self.client.get(archive_url, coll_data)

        self.assert_(response['Location'].endswith('%s?collection=%s' % \
            (reverse('collection:browse-archive', kwargs={'archive': coll_data['archive']}),
            coll_data['collection'])),
            'should redirect to archive browse with collection filter when multiple results are found')
        self.assertEqual(303, response.status_code,
            'find collection should redirect with 303 when multiple matches are found, got %s' \
            % response.status_code)

        # retrieve index page to test messages
        response = self.client.get(reverse('site-index'))
        msg = list(response.context['messages'])[0]
        self.assertEqual('3 collections found for MARBL 1000.', str(msg),
            'user should see message indicating more than one collection was found')
        self.assertEqual('info', msg.tags,
            'message should be of type info')

        # mimic zero results found
        mockcollq.count.return_value = 0
        # search by archive & id
        coll_data = {'archive': 'marbl', 'collection': '1000'}
        response = self.client.get(archive_url, coll_data)

        self.assertEqual(200, response.status_code,
            'find collection should NOT redirect when no matches are found, got %s' \
            % response.status_code)

        # check for warning message
        msg = list(response.context['messages'])[0]
        self.assertEqual('No collections found for MARBL 1000.', str(msg),
            'user should see message indicating more than one collection was found')
        self.assertEqual('warning', msg.tags,
            'message should be of type warning')


        # mimic invalid form submission
        response = self.client.get(archive_url, {'archive': '', 'collection': '1'})

        self.assertEqual(200, response.status_code,
            'find collection should NOT redirect when form is invalid are found, got %s' \
            % response.status_code)

        # check for warning message
        msg = list(response.context['messages'])[0]
        self.assertEqual('Collection search input was not valid; please try again.',
            str(msg),
            'user should see message indicating more than one collection was found')
        self.assertEqual('warning', msg.tags,
            'message should be of type warning')



    @patch('keep.collection.views.solr_interface')
    @patch('keep.collection.views.Paginator')
    def test_browse_archive(self, mockpaginator, mocksolr_interface):
        browse_url = reverse('collection:browse-archive', kwargs={'archive': 'marbl'})

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        archive_obj = self.repo.get_object(settings.PID_ALIASES['marbl'])

        # setup solr mock
        mocksolr = mocksolr_interface.return_value
        mocksolr.query.return_value = mocksolr.query
        for method in ['query', 'filter', 'sort_by', 'join']:
            getattr(mocksolr.query, method).return_value = mocksolr.query

        # set mock facet results via paginator
        mockpage = NonCallableMock()
        mockpaginator.return_value.page.return_value = mockpage
        mockpage.paginator.page_range = [1]
        mockpage.paginator.count = 4
        mockpage.start_index = 1
        mockpage.end_index = 4
        mockpage.object_list = [
            {'pid': 'pid:1', 'title': 'foo', 'source_id': 0, 'label': 'foo',
            'date': ('2001-01-30T01:22:11z', '1980')},
            {'pid': 'pid:2', 'title': 'bar', 'source_id': 11, 'label': 'bar',
            'date': ('2011-04-26T20:44:56.421999Z', '1985-1990')},
            {'pid': 'pid:3', 'title': 'baz', 'source_id': 12, 'label': 'baz',
            'date': ('2001-01-30T01:22:12z', '1509-1805')},
            {'pid': 'pid:4', 'title': '', 'source_id': 13, 'label': '',
            'date': (u'1855-1861', u'2011-04-26T20:40:14.336000Z')},
        ]


        # initial solr query generated in collection objet class, so must be patched there
        with patch('keep.collection.views.CollectionObject.item_collection_query') as \
          mock_item_collection_query:
            mock_item_collection_query.return_value = mocksolr.query
            response = self.client.get(browse_url)

            # check solr query/filters

            mocksolr.query.query.assert_called_with(archive_id=settings.PID_ALIASES['marbl'])
            mocksolr.query.sort_by.assert_called_with('source_id')

            # TODO: test join queries?

        self.assertEqual(mockpage, response.context['collections'],
            'paginated solr result should be set as collections in response context')

        # basic display checking
        # - archive label, link to list
        self.assertContains(response, archive_obj.label,
            msg_prefix='collections by archive page should include archive name')
        self.assertContains(response, reverse('collection:list-archives'),
            msg_prefix='collections by archive page should link to full archive list')

        # - collection display
        for item in mockpage.object_list:
            coll_view_url = reverse('collection:view', kwargs={'pid': item['pid']})
            self.assertContains(response, coll_view_url,
                msg_prefix='collection view url should be included in the browse page')

            self.assertContains(response, coll_view_url,
                    msg_prefix='collection view url should be included in browse page')
            # first result has source id 0, should not be displayed
            if item['source_id'] == 0:
                self.assertContains(response, '<h2 class="media-heading">%s</h2>' % item['title'],
                    html=True,
                    msg_prefix='collection title should be displayed without source id when it is 0')

            else:
                self.assertContains(response, '<h2 class="media-heading">%s: %s</h2>' % \
                        (item['source_id'], item['title'] or '(no title present)'),
                    html=True,
                    msg_prefix='collection title should be displayed with source id when set')

        # date or date range should be displayed no matter what order is returned
        self.assertContains(response, mockpage.object_list[0]['date'][1])
        self.assertContains(response, mockpage.object_list[1]['date'][1])
        self.assertContains(response, mockpage.object_list[2]['date'][1])
        self.assertContains(response, mockpage.object_list[3]['date'][0])

        # errors
        # - pid alias in config but not in fedora should 404
        with patch('keep.collection.views.Repository') as mockrepo:
            mockrepo.return_value.get_object.return_value.exists = False
            response = self.client.get(browse_url)
            expected, got = 404, response.status_code
            self.assertEqual(expected, got,
                'expected %s but got %s for browse archive with alias not in pid alias config' % \
                (expected, got))

        # - pid alias not in config should 404
        browse_url = reverse('collection:browse-archive', kwargs={'archive': 'bogus'})
        response = self.client.get(browse_url)
        expected, got = 404, response.status_code
        self.assertEqual(expected, got,
            'expected %s but got %s for browse archive with alias not in pid alias config' % \
            (expected, got))

        # logout to test guest/researcher access
        browse_url = reverse('collection:browse-archive', kwargs={'archive': 'marbl'})
        self.client.logout()
        response = self.client.get(browse_url)
        expected, got = 302, response.status_code
        self.assertEqual(expected, got,
            'Expected status code %s when accessing %s as guest, got %s' % \
            (expected, got, browse_url))
        self.assert_(reverse('accounts:login') in response['Location'],
            'guest access to search should redirect to login page')

        # create researcher IP for localhost so anonymous access will be
        # treated as anonymous researcher
        researchip = ResearcherIP(name='test client', ip_address='127.0.0.1')
        researchip.save()
        with patch('keep.collection.views.CollectionObject.item_collection_query') as \
          mock_item_collection_query:
            mock_item_collection_query.return_value = mocksolr.query
            response = self.client.get(browse_url)

            # check that join query for researcher perms was called
            mocksolr.query.join.assert_any_call('collection_id', 'pid', researcher_access=True)
            mocksolr.query.join.assert_any_call('collection_id', 'pid', has_access_copy=True)

            # basic check that page renders (i.e., no permissions redirect)
            self.assertContains(response, archive_obj.label,
                msg_prefix='collections by archive page should include archive name')

            # simulate no researcher accessible perms - should prompt login
            mocksolr.query.count.return_value = 0
            response = self.client.get(browse_url)
            expected, got = 302, response.status_code
            self.assertEqual(expected, got,
                'Expected status code %s when accessing %s with no researcher-accessible content as researcher, got %s' % \
                (expected, got, browse_url))
            self.assert_(reverse('accounts:login') in response['Location'],
                'non-researcher accessible archive should redirect to login page')

        researchip.delete()

    def test_raw_datastream(self):
        obj = FedoraFixtures.rushdie_collection()
        obj.save()  # save to fedora for editing
        self.pids.append(obj.pid)

        self.client.login(**ADMIN_CREDENTIALS)

        # NOTE: not testing strenuously here because this view is basically a
        # wrapper around a generic eulfedora view

        # MODS
        ds_url = reverse('collection:raw-ds', kwargs={'pid': obj.pid, 'dsid': 'MODS'})
        response = self.client.get(ds_url)
        expected, got = 200, response.status_code
        self.assertEqual(expected, got,
            'Expected %s but returned %s for %s (MODS datastream)' \
                % (expected, got, ds_url))
        # RELS-EXT
        ds_url = reverse('collection:raw-ds', kwargs={'pid': obj.pid, 'dsid': 'RELS-EXT'})
        response = self.client.get(ds_url)
        expected, got = 200, response.status_code
        self.assertEqual(expected, got,
            'Expected %s but returned %s for %s (RELS-EXT datastream)' \
                % (expected, got, ds_url))

        # DC
        ds_url = reverse('collection:raw-ds', kwargs={'pid': obj.pid, 'dsid': 'DC'})
        response = self.client.get(ds_url)
        expected, got = 200, response.status_code
        self.assertEqual(expected, got,
            'Expected %s but returned %s for %s (DC datastream)' \
                % (expected, got, ds_url))

    def test_audit_trail(self):
        # test object with ingest message
        obj = FedoraFixtures.rushdie_collection()
        obj.save('audit trail test')
        self.pids.append(obj.pid)

        self.client.login(**ADMIN_CREDENTIALS)

        audit_url = reverse('collection:audit-trail', kwargs={'pid': obj.pid})
        response = self.client.get(audit_url)
        expected, got = 200, response.status_code
        self.assertEqual(expected, got,
            'Expected %s but returned %s for %s (raw audit trail xml)' \
                % (expected, got, audit_url))
        self.assertContains(response, 'justification>audit trail test</audit')

    @patch('keep.collection.views.solr_interface')
    def test_suggest(self, mock_solr_interface):
        solrquery = mock_solr_interface.return_value
        solrquery.query.return_value = solrquery
        solrquery.filter.return_value = solrquery
        solrquery.field_limit.return_value = solrquery
        solrquery.sort_by.return_value = solrquery

        self.client.login(**ADMIN_CREDENTIALS)
        suggest_url = reverse('collection:suggest')

        # no search term - empty result
        response = self.client.get(suggest_url)
        self.assertEqual('application/json', response['Content-Type'],
                         'suggest view should return json content')
        # inspect result
        data = json.loads(response.content)
        self.assertEqual([], data,
                         'suggest should return empty list for no search term')
        # solr should not be called when there is no search term
        solrquery.assert_not_called()

        # sample solr results to test json return construction
        result = [
            {'pid': 'test:1', 'title': 'Rushdie Papers'},
            {'pid': 'test:2', 'title': 'Salman Rushdie Collection',
             'source_id': '1000', 'archive_short_name': 'MARBL',
             'creator': 'Rushdie, Salman'}
        ]
        solrquery.__getitem__.return_value = result
        # search term, inspect query args and json result
        response = self.client.get(suggest_url, {'term': '1000 rushd'})
        solrquery.filter.assert_any_call(content_model=CollectionObject.COLLECTION_CONTENT_MODEL)
        solrquery.filter.assert_any_call(archive_id__any=True)
        solrquery.field_limit.assert_called_with(['pid', 'source_id', 'title',
                                                        'archive_short_name', 'creator', 'archive_id'])
        solrquery.sort_by.assert_called_with('-score')
        # search terms
        solrquery.query.assert_called_with(['1000', 'rushd*'])
        data = json.loads(response.content)
        self.assertEqual(result[0]['pid'], data[0]['value'],
                         'value should be set as item pid')
        self.assertEqual(' ' + result[0]['title'], data[0]['label'],
                         'label sholud be item title when there is no source id')
        # second result has source id
        self.assertEqual('%s %s' % (result[1]['source_id'],
                                    result[1]['title']), data[1]['label'],
                         'label should be source id + title when both are present')
        # description - should use creator, if any
        self.assertEqual('', data[0]['desc'])
        self.assertEqual(result[1]['creator'], data[1]['desc'])
        # category - should use archive short name, if any
        self.assertEqual('', data[0]['category'])
        self.assertEqual(result[1]['archive_short_name'], data[1]['category'])

        # if wildcard returns no results, should try again without wildcard
        solrquery.count.return_value = 0
        response = self.client.get(suggest_url, {'term': '1000 rushd'})
        # should query with the wildcard, then without when count is 0
        solrquery.query.assert_any_call(['1000', 'rushd*'])
        solrquery.query.assert_any_call(['1000', 'rushd'])

    @patch('keep.collection.views.CollectionObject.solr_items_query')
    @patch('keep.collection.views.Paginator')
    def test_view(self, mockpaginator, mocksolr_items):
        # configure solr response for collection item query
        mockquery = mocksolr_items.return_value
        mockquery.return_value = mockquery
        for method in ['query', 'field_limit', 'sort_by', 'filter']:
            getattr(mockquery, method).return_value = mockquery
        solr_response = mockquery.execute.return_value
        solr_response.result.numFound = 0
        # set mock results via paginator
        mockpage = NonCallableMock()
        mockpage.paginator.page_range = [1]
        mockpage.paginator.count = 0
        # mockpage.start_index = 1
        # mockpage.end_index = 1
        mockpaginator.return_value.page.return_value = mockpage
        mockpage.object_list = []

        # log in as staff (TODO: support researcher access)
        # NOTE: using admin view so user credentials will be used to access fedora
        self.client.post(settings.LOGIN_URL, ADMIN_CREDENTIALS)

        # load fixture collection for display
        # repo = Repository()
        obj = FedoraFixtures.rushdie_collection()
        # store initial collection id from fixture
        # collection_uri = obj.collection.uri
        obj.save()  # save to fedora for editing
        self.pids.append(obj.pid)

        coll_view_url = reverse('collection:view', kwargs={'pid': obj.pid})
        response = self.client.get(coll_view_url)
        # inspect solr query
        # NOTE: not testing collection filter because that happens in model method
        # FIXME: worth testing order here?
        mockquery.sort_by.assert_any_call('date_created')
        mockquery.sort_by.assert_any_call('date_issued')
        mockquery.sort_by.assert_any_call('title_exact')
        self.assertContains(response, obj.mods.content.title,
            msg_prefix='collection view should include collection title')
        self.assertContains(response, obj.mods.content.source_id,
            msg_prefix='collection view should include collection number')
        # TODO: edit link only present based on user perms
        self.assertContains(response, reverse('collection:edit', kwargs={'pid': obj.pid}),
            msg_prefix='collection view should include link to collection edit page')

        self.assertContains(response, obj.collection.label.replace('&', '&amp;'),
            msg_prefix='collection view should display parent archive label')
        self.assertContains(response,
            reverse('collection:browse-archive',
                     kwargs={'archive': obj.collection.mods.content.short_name.lower()}),
            msg_prefix='collection view should link to parent archive browse')
        self.assertContains(response,
            reverse('collection:list-archives'),
            msg_prefix='collection view should link to top-level archive browse')
        self.assertContains(response, 'No items in this collection',
            msg_prefix='collection view indicate no items when solr returns no results')

        # test 404
        boguscoll_view_url = reverse('collection:view', kwargs={'pid': 'bogus:1234'})
        response = self.client.get(boguscoll_view_url)
        expected, got = 404, response.status_code
        self.assertEqual(expected, got,
            'Expected status code %s when accessing %s (non-existent pid), got %s' % \
            (expected, boguscoll_view_url, got))

        # test with 1 simulated item in collection; setting mock results via paginator
        solr_response.result.numFound = 1
        mockpage.paginator.page_range = [1]
        mockpage.paginator.count = 1
        mockpage.start_index = 1
        mockpage.end_index = 4

        mockpage.object_list = [
            {'pid': 'pid:1', 'title': 'foo', 'source_id': 0, 'label': 'foo',
            'date': ('2001-01-30T01:22:11z', '1980'), 'object_type': 'audio',
            'duration': 65,
            'content_model': [AudioObject.AUDIO_CONTENT_MODEL,] },
        ]
        response = self.client.get(coll_view_url)
        self.assertContains(response, '<h2 class="section-heading">1 item in this collection</h2>',
            html=True, msg_prefix='count of items in collection should be displayed')
        self.assertContains(response, 'glyphicon-headphones',
            msg_prefix='headphone glyph should be used for audio item')
        self.assertContains(response, mockpage.object_list[0]['title'],
            msg_prefix='item title should be displayed')
        self.assertContains(response, '1 minute, 5 seconds',
            msg_prefix='audio item duration should be diplayed in human readable format')
        self.assertContains(response, reverse('audio:view', kwargs={'pid': mockpage.object_list[0]['pid']}),
            msg_prefix='link to view page for audio item title should be present')
        # TODO: only present if user has edit permissions
        self.assertContains(response, reverse('audio:edit', kwargs={'pid': mockpage.object_list[0]['pid']}),
            msg_prefix='link to edit page for audio item title should be present')

        # logout to test guest/researcher access
        self.client.logout()
        response = self.client.get(coll_view_url)
        expected, got = 302, response.status_code
        self.assertEqual(expected, got,
            'Expected status code %s when accessing %s as guest, got %s' % \
            (expected, coll_view_url, got))
        self.assert_(reverse('accounts:login') in response['Location'],
            'guest access to collection view should redirect to login page')

        # create researcher IP for localhost so anonymous access will be
        # treated as anonymous researcher
        researchip = ResearcherIP(name='test client', ip_address='127.0.0.1')
        researchip.save()

        response = self.client.get(coll_view_url)
        # spot-check that response displays correctly
        self.assertContains(response, '<h2 class="section-heading">1 item in this collection</h2>',
            html=True, msg_prefix='count of items in collection should be displayed')

        # simulate no researcher-accessible content - should get permission error
        mockquery.count.return_value = 0
        response = self.client.get(coll_view_url)
        expected, got = 302, response.status_code
        self.assertEqual(expected, got,
            'Expected status code %s when accessing collection with no researcher-accessible items as researcher, got %s' % \
            (expected, got))
        self.assert_(reverse('accounts:login') in response['Location'],
            'guest access to collection view should redirect to login page')

        researchip.delete()


class FindingAidTest(KeepTestCase):
    exist_fixtures = {'directory':  path.join(path.dirname(path.abspath(__file__)), 'fixtures')}
    marbl = 'Manuscript, Archives, and Rare Book Library'

    def test_find_by_unitid(self):
        found = FindingAid.find_by_unitid('244', self.marbl)
        self.assert_(isinstance(found, FindingAid),
            'find_by_unitid [244, MARBL] found and returned a single FindingAid object')
        # should be the document we expect
        self.assert_('Abbey Theatre' in unicode(found.title),
            'find_by_unitid("244") should find Abbey Theater EAD document')

        # missing/no match
        self.assertRaises(Exception, FindingAid.find_by_unitid, '301023', self.marbl)

        # partial/non-exact match
        self.assertRaises(Exception, FindingAid.find_by_unitid, '24', self.marbl)

    def test_generate_collection(self):
        abbey = FindingAid.find_by_unitid('244', self.marbl)
        coll = abbey.generate_collection()
        self.assert_(isinstance(coll, CollectionObject))
        # title
        self.assertEqual('Abbey Theatre collection', coll.mods.content.title)
        # name / main entry
        self.assertEqual('Abbey Theatre.', coll.mods.content.name.name_parts[0].text)
        self.assertEqual('corporate', coll.mods.content.name.type)
        self.assertEqual('naf', coll.mods.content.name.authority)

        # coverage / dates - abbey244 fixture has 1921/1995
        self.assertEqual('1921', coll.mods.content.origin_info.created[0].date)
        self.assertEqual('start', coll.mods.content.origin_info.created[0].point)
        self.assertEqual('w3cdtf', coll.mods.content.origin_info.created[0].encoding)
        self.assertEqual(True, coll.mods.content.origin_info.created[0].key_date)
        self.assertEqual('1995', coll.mods.content.origin_info.created[1].date)
        self.assertEqual('end', coll.mods.content.origin_info.created[1].point)
        self.assertEqual('w3cdtf', coll.mods.content.origin_info.created[1].encoding)
        # TODO: test single date

        # source id
        self.assertEqual(244, coll.mods.content.source_id)

        # access restrictions
        self.assertEqual('Unrestricted access.', coll.mods.content.restrictions_on_access.text)
        # TODO: test multi-paragraph restriction

        # use & reproduction
        self.assert_('Information on copyright (literary rights) available' in
             coll.mods.content.use_and_reproduction.text)
        self.assert_('limitations noted in departmental policies' in
             coll.mods.content.use_and_reproduction.text)

        # generated MODS should be schema-valid
        self.assert_(coll.mods.content.is_valid())

        # gregory624 - family name for main entry/origination
        gregory = FindingAid.find_by_unitid('624', self.marbl)
        coll = gregory.generate_collection()
        # name / main entry type
        self.assertEqual('family', coll.mods.content.name.type)
        self.assertEqual('Gregory family', coll.mods.content.name.name_parts[0].text)

        # rushdie1000
        # - personal name, single coverage date (for test), multi-paragraph restrictions
        rushdie = FindingAid.find_by_unitid('1000', self.marbl)
        coll = rushdie.generate_collection()
        self.assertEqual('personal', coll.mods.content.name.type)
        # coverage / dates - fixture has 1947
        self.assertEqual('1947', coll.mods.content.origin_info.created[0].date)
        self.assertEqual(None, coll.mods.content.origin_info.created[0].point)
        self.assertEqual('w3cdtf', coll.mods.content.origin_info.created[0].encoding)
        self.assertEqual(True, coll.mods.content.origin_info.created[0].key_date)
        # only one date added
        self.assertEqual(1, len(coll.mods.content.origin_info.created))
        # multi-paragraph restrictions on access
        # - first paragraph
        self.assert_('The following series are completely closed'
            in coll.mods.content.restrictions_on_access.text)
        # - middle somewhere
        self.assert_('Subseries 7.4: Family photographs'
            in coll.mods.content.restrictions_on_access.text)
        # - last paragraph
        self.assert_('7.3: Slides and negatives'
            in coll.mods.content.restrictions_on_access.text)
        # multi-paragraph use restrictions
        # - first paragraph
        self.assert_('The use of personal cameras is not allowed'
            in coll.mods.content.use_and_reproduction.text)
        # - second/last paragraph
        self.assert_('not permitted to copy or download any digital files'
            in coll.mods.content.use_and_reproduction.text)


class SimpleCollectionTest(KeepTestCase):
    def setUp(self):
        self.repo = Repository()
        self.pids = []

        # Create fixtures and add to pid list
        self.simple_collection_1 = FedoraFixtures.simple_collection(label='Test Simple Collection 1',
            status='Processed')
        self.simple_collection_1.save()
        self.pids.append(self. simple_collection_1.pid)

        self.simple_collection_2 = FedoraFixtures.simple_collection(label='Test Simple Collection 2',
            status='Accessioned')
        self. simple_collection_2.save()
        self.pids.append(self.simple_collection_2.pid)

        # Create user for tests
        user = get_user_model()(username="euterpe")
        user.set_password("digitaldelight")
        user.is_active = True
        user.is_superuser = True
        user.save()

    def tearDown(self):
        for pid in self.pids:
            try:
                self.repo.purge_object(pid)
            except RequestFailed:
                logger.warning('Failed to purge %s in tearDown' % pid)

    def test_creation(self):
        obj = self.repo.get_object(type=SimpleCollection)
        obj.mods.content.create_restrictions_on_access()
        obj.mods.content.restrictions_on_access.text = 'processed'
        saved = obj.save()
        self.pids.append(obj.pid)

        self.assertTrue(saved)
        self.assertEqual(obj. COLLECTION_CONTENT_MODEL, 'info:fedora/emory-control:Collection-1.0')
        self.assertEqual(obj.mods.content.restrictions_on_access.text, 'processed')

        self.assertTrue((obj.uriref, RDF.type, REPO.SimpleCollection) in obj.rels_ext.content,
                        'The collection is of type SimpleCollection')

        # init non-existent pid
        # should not raise exception by trying to set type
        self.repo.get_object(type=SimpleCollection, pid='foo:1')

    def test__objects_by_type(self):
        # run an RIsearch query with flush changes so test does not fail
        # when syncUpdates is turned off
        self.repo.risearch.count_statements('* * *', flush=True)

        # NOTE: since we no longer have a dedicated test fedora for unit tests,
        # this runs against the dev fedora, which could contain other
        # "simple collection" objects; filter by configured (test) pidspace
        # to just the objects we expect
        def filter_by_pidspace(obj_list):
            return [o for o in obj_list
                    if o.pid.startswith('%s:' % settings.FEDORA_PIDSPACE)]

        # Test Simple collection
        objs = _objects_by_type(REPO.SimpleCollection, SimpleCollection)
        obj_list = filter_by_pidspace(objs)
        self.assertTrue(len(obj_list) == 2)
        self.assertTrue(isinstance(obj_list[0], SimpleCollection),
                        "object is of type SimpleCollection")

        # Test Simple collection wtith no obj type
        objs = _objects_by_type(REPO.SimpleCollection)
        obj_list = filter_by_pidspace(objs)
        self.assertTrue(len(obj_list) == 2)
        self.assertTrue(isinstance(obj_list[0], DigitalObject), "object is of type DigitalObject")

        # Test invalid type
        objs = _objects_by_type(REPO.FakeType)
        obj_list = filter_by_pidspace(objs)
        self.assertTrue(len(obj_list) == 0)

    def test_edit(self):
        self.client.post(settings.LOGIN_URL, ADMIN_CREDENTIALS)
        edit_url = reverse('collection:simple_edit',
            kwargs={'pid': self.simple_collection_2.pid})
        response = self.client.get(edit_url)
        expected, code = 200, response.status_code
        self.assertEqual(code, expected, 'Expected %s but returned %s' % (expected, code))

        self.assertContains(response, self.simple_collection_2.label)
        self.assertContains(response, 'Accessioned', msg_prefix='Status of collection should be Accessioned')

    def test_browse(self):
        # run an RIsearch query with flush changes so test does not fail
        # when syncUpdates is turned off
        self.repo.risearch.count_statements('* * *', flush=True)

        self.client.post(settings.LOGIN_URL, ADMIN_CREDENTIALS)
        browse_url = reverse('collection:simple_browse')
        response = self.client.get(browse_url)
        expected, code = 200, response.status_code
        self.assertEqual(code, expected, 'Expected %s but returned %s' % (expected, code))

        self.assertContains(response, self.simple_collection_1.label)
        self.assertContains(response, self.simple_collection_1.pid)
        self.assertContains(response, self.simple_collection_2.label)
        self.assertContains(response, self.simple_collection_2.pid)


class TestBatchUpdateStatusTask(KeepTestCase):

    def setUp(self):
        self.repo = Repository()
        self.pids = []

        #create ArrengementObject and associate to a collection
        self.arrangement_1 = self.repo.get_object(type=ArrangementObject)
        self.arrangement_1.label = "Test Arrangement Object 1"
        self.arrangement_1.state = 'I'
        self.arrangement_1.save()
        self.pids.append(self.arrangement_1.pid)

        self.arrangement_2 = self.repo.get_object(type=ArrangementObject)
        self.arrangement_2.label = "Test Arrangement Object 2"
        self.arrangement_2.state = 'I'
        self.arrangement_2.save()
        self.pids.append(self.arrangement_2.pid)

        #Create fixtures and add to pid list
        self.simple_collection_1 = FedoraFixtures.simple_collection(label='Test Simple Collection 1',
            status='Processed')
        self.simple_collection_1.save()
        self.pids.append(self.simple_collection_1.pid)

        self.simple_collection_2 = FedoraFixtures.simple_collection(label='Test Simple Collection 2',
            status='Accessioned')
        # add arrangements to collection
        self.simple_collection_2.rels_ext.content.add((self.simple_collection_2.uriref,
                                                       relsext.hasMember, self.arrangement_1.uriref))
        self.simple_collection_2.rels_ext.content.add((self.simple_collection_2.uriref,
                                                       relsext.hasMember, self.arrangement_2.uriref))
        self. simple_collection_2.save()
        self.pids.append(self.simple_collection_2.pid)

    def tearDown(self):
        for pid in self.pids:
            self.repo.purge_object(pid)


    def test_batch_update_objects(self):
        status = 'Processed'
        result = batch_set_status(self.simple_collection_2.pid, status)
        self.assertEqual('Successfully updated 2 items', result)
        arr1 = self.repo.get_object(pid=self.arrangement_1.pid, type=ArrangementObject)
        self.assertEqual('Marking as %s via SimpleCollection %s' % (status, self.simple_collection_2.pid),
                         arr1.audit_trail.records[-1].message,
                         'audit trail message should indicate why status was changed')
        self.assertEqual(arr1.state, 'A')
        self.assertEqual(self.repo.get_object(pid=self.arrangement_1.pid, type=ArrangementObject).state, 'A')

        status = 'Accessioned'
        result = batch_set_status(self.simple_collection_2.pid, status)
        self.assertEqual('Successfully updated 2 items', result)
        self.assertEqual(self.repo.get_object(pid=self.arrangement_1.pid, type=ArrangementObject).state, 'I')
        self.assertEqual(self.repo.get_object(pid=self.arrangement_2.pid, type=ArrangementObject).state, 'I')

        # when bad status is given, nothing should change
        self.assertRaises(Exception, batch_set_status, self.simple_collection_2.pid, 'badstatus')
        # item state unchanged
        self.assertEqual(self.repo.get_object(pid=self.arrangement_1.pid, type=ArrangementObject).state, 'I')
        self.assertEqual(self.repo.get_object(pid=self.arrangement_2.pid, type=ArrangementObject).state, 'I')
