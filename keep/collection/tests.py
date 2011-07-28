from contextlib import contextmanager
import logging
from mock import Mock, patch
from os import path
from rdflib import URIRef
from rdflib.namespace import RDF
from sunburnt import sunburnt

from django.conf import settings
from django.core.urlresolvers import reverse, resolve
from django.test import Client
from django.utils import simplejson

from eulfedora.rdfns import relsext
from eulfedora.util import RequestFailed


from keep.arrangement.models import ArrangementObject
from keep.collection.fixtures import FedoraFixtures
from keep.collection import forms as cforms
from keep.collection import views
from keep.collection.models import CollectionObject, CollectionMods, FindingAid, SimpleCollection
from keep.collection.views import _objects_by_type
from keep.common.fedora import DigitalObject, Repository
from keep.common.rdfns import REPO
from keep import mods
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

    @patch('keep.collection.models.sunburnt')
    def test_archives(self, mocksunburnt):
        # NOTE: mock order/syntax depends on how it is used in the method
        solrquery = mocksunburnt.SolrInterface.return_value.query
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

    def test_collection_info(self):
        # test setting & getting collection membership
        obj = self.repo.get_object(type=CollectionObject)
        self.assertEqual(None, obj.collection_id,
            "CollectionObject with no collection membership returns None for collection id")
        self.assertEqual(None, obj.collection_label,
            "CollectionObject with no collection membership returns None for collection label")

        # set collection membership
        collections = FedoraFixtures.archives()
        obj.set_collection(collections[0].uri)
        self.assertEqual(collections[0].uri, obj.collection_id)
        # use fixture archives instead of the real one for label look-up
        with patch('keep.collection.models.CollectionObject.archives',
                   new=Mock(return_value=FedoraFixtures.archives())):
            self.assertEqual(collections[0].label, obj.collection_label)

        # update collection membership
        obj.set_collection(collections[1].uri)
        self.assertEqual(collections[1].uri, obj.collection_id)
        with patch('keep.collection.models.CollectionObject.archives',
                   new=Mock(return_value=FedoraFixtures.archives())):
            self.assertEqual(collections[1].label, obj.collection_label)

    def test_update_dc(self):
        # DC should get updated from MODS & RELS-EXT on save

        # create test object and populate with data
        obj = self.repo.get_object(type=CollectionObject)
        # collection membership in RELS-EXT
        collections = FedoraFixtures.archives()
        obj.set_collection(collections[0].uri)
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

        pids = [ self.rushdie.pid, self.esterbrook.pid, self.engdocs.pid ]
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

    @patch('keep.collection.models.sunburnt.SolrInterface', mocksolr)
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

    @patch('keep.collection.models.sunburnt.SolrInterface', mocksolr)
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

    @patch('keep.collection.models.sunburnt.SolrInterface', mocksolr)
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
        self.assertEqual(parent_collection, kwargs['collection_id'],
            'find by mss number with parent option should filter on collection_id')

        # empty result
        self.mocksolr.query.execute.return_value = []
        found = list(CollectionObject.find_by_collection_number(search_coll, parent_collection))
        self.assertEqual([], found,
            'when solr returns no results, find by collection number returns an empty list')

    def test_index_data_descriptive(self):
        # test descriptive metadata used for indexing objects in solr

        # use a mock object to simulate pulling archive object from Fedora
        mockarchive = Mock(CollectionObject)
        mockarchive.label = 'MARBL'
        
        # create test object and populate with data
        obj = self.repo.get_object(type=CollectionObject)
        obj._collection_id = 'parent:1'
        obj.dc.content.title = 'test collection'

        # test index data for parent archive separately
        # so we can mock the call to initialize the parent CollectionObject
        with patch('keep.collection.models.CollectionObject',
                   new=Mock(return_value=mockarchive)):
            arch_data = obj._index_data_archive()
            self.assertEqual(obj.collection_id, arch_data['archive_id'],
                             'parent collection object (archive) id should be set in index data')
            self.assertEqual(mockarchive.label, arch_data['archive_label'],
                             'parent collection object (archive) label should be set in index data')
            # error if data is not serializable as json
            self.assert_(simplejson.dumps(arch_data))

        # skip index archive data and test the rest
        obj._index_data_archive = Mock(return_value={})
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
        self.assert_(simplejson.dumps(desc_data))


# sample POST data for creating a collection
COLLECTION_DATA = {
    'title': 'Rushdie papers',
    'source_id': '1000',
    'date_created': '1947',
    'date_end': '2008',
    'collection': 'info:fedora/emory:93z53',
    'resource_type': 'mixed material',
    'use_and_reproduction-text': 'no photos',
    'restrictions_on_access-text': 'tuesdays only',
    'name-type': 'personal',
    'name-authority': 'local',
    # 'management' form data is required for django to process formsets
    'name-name_parts-INITIAL_FORMS': '0',
    'name-name_parts-TOTAL_FORMS': '1',
    'name-name_parts-MAX_NUM_FORMS': '',
    'name-name_parts-0-text':'Mr. So and So',
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
        # store initial collection id from fixture
        self.collection_uri = self.obj.collection_id


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

    def test_update_instance(self):
        # test custom save logic for date created
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
        data['collection'] = self.archives[2].uri
        form = cforms.CollectionForm(data, instance=self.obj)
        self.assertTrue(form.is_valid(), "test form object with test data is valid")
        form.update_instance()
        self.assertEqual(self.archives[2].uri, self.obj.collection_id)

    def test_initial_data(self):
        form = cforms.CollectionForm(instance=self.obj)
        # custom fields that are not handled by XmlObjectForm have special logic
        # to ensure they get set when an instance is passed in
        expected, got = self.collection_uri, form.initial['collection']
        self.assertEqual(expected, got,
            'collection uri is set correctly in form initial data from instance; expected %s, got %s' \
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
    fixtures =  ['users']

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

    def test_create(self):
        # test creating a collection object
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

        # POST and create new object, verify in fedora
        data = COLLECTION_DATA.copy()
        data['_save_continue'] = True   # use 'save and continue' so we can get created object from response
        response = self.client.post(new_coll_url, data, follow=True)
        # do we need to test actual response, redirect ?
        messages = [ str(msg) for msg in response.context['messages'] ]
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
                      URIRef(COLLECTION_DATA['collection'])) in
                      new_coll.rels_ext.content,
                      "collection object is member of requested top-level collection")

        # confirm that current site user appears in fedora audit trail
        xml, uri = new_coll.api.getObjectXML(new_coll.pid)
        self.assert_('<audit:responsibility>%s</audit:responsibility>' % ADMIN_CREDENTIALS['username'] in xml)


    def test_edit(self):
        repo = Repository()
        obj = FedoraFixtures.rushdie_collection()
        # store initial collection id from fixture
        collection_uri = obj.collection_id
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
        self.assert_(isinstance(response.context['form'].instance, CollectionMods),
                "form instance is a collection MODS XmlObject")
        self.assertContains(response, 'value="1000"',
                msg_prefix='MSS # from existing object set as input value')
        self.assertContains(response, 'value="Salman Rushdie Collection"',
                msg_prefix='Title from existing object set as input value')
        self.assertContains(response, 'value="1947"',
                msg_prefix='Start date from existing object set as input value')
        self.assertContains(response, 'value="2008"',
                msg_prefix='End date from existing object set as input value')
        self.assertContains(response, 'value="%s" selected="selected"' % collection_uri,
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
        messages = [ str(msg) for msg in response.context['messages'] ]
        self.assert_(messages[0].startswith('Successfully updated collection'),
            'successful collection update message displayed to user')
        self.assert_(obj.pid in messages[0],
            'success message includes object pid')
        obj = repo.get_object(type=CollectionObject, pid=obj.pid)
        self.assertEqual(COLLECTION_DATA['title'], obj.mods.content.title,
            "MODS content updated in existing object from form data")
        # confirm that current site user appears in fedora audit trail
        xml, uri = obj.api.getObjectXML(obj.pid)
        self.assert_('<audit:responsibility>%s</audit:responsibility>' % ADMIN_CREDENTIALS['username'] in xml,
            'user logged into site is also username in fedora audit:trail')

        # test logic for save and continue editing
        data = COLLECTION_DATA.copy()
        data['_save_continue'] = True   # simulate submit via 'save and continue' button
        response = self.client.post(edit_url, data)
        messages = [ str(msg) for msg in response.context['messages'] ]
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
        messages = [ str(msg) for msg in response.context['messages'] ]
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

        messages = [ str(msg) for msg in response.context['messages'] ]
        self.assert_('Successfully created collection' in messages[0],
            'successful collection creation message displayed to user on save and continue editing')

        # attempt to edit non-existent record
        edit_url = reverse('collection:edit', args=['my-bogus-pid:123'])
        response = self.client.get(edit_url)
        expected, code = 404, response.status_code
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s (non-existing pid)'
                             % (expected, code, edit_url))

    @patch('keep.collection.views.sunburnt')
    def test_search(self, mocksunburnt):
        search_url = reverse('collection:search')

        # using a mock for sunburnt so we can inspect method calls,
        # simulate search results, etc.

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        default_search_args = {
            'pid': '%s:*' % settings.FEDORA_PIDSPACE,
            'content_model': CollectionObject.COLLECTION_CONTENT_MODEL,
        }

        # search all collections (no user-entered search terms)
        response = self.client.get(search_url)
        args, kwargs = mocksunburnt.SolrInterface.return_value.query.call_args
        # default search args that should be included on every collection search
        self.assertEqual(CollectionObject.COLLECTION_CONTENT_MODEL, kwargs['content_model'],
                         'collection search should be filtered by collection content model')
        self.assertEqual('%s:*' % settings.FEDORA_PIDSPACE, kwargs['pid'],
                         'collection search should be filtered by configured pidspace')

        # search by MSS # (AKA source id)
        mss = 1000
        response = self.client.get(search_url, {'collection-source_id': mss})
        args, kwargs = mocksunburnt.SolrInterface.return_value.query.call_args
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
        args, kwargs = mocksunburnt.SolrInterface.return_value.query.call_args
        self.assertEqual(search_title, kwargs['title'],
                         'title search term should be included in solr query terms')
        self.assert_('source_id' not in kwargs)
        self.assertEqual(search_title, response.context['search_info']['title'],
                         'title search term should be included in search info for display to user')        

        # search by creator
        creator = 'esterbrook'
        response = self.client.get(search_url, {'collection-creator': creator})
        args, kwargs = mocksunburnt.SolrInterface.return_value.query.call_args
        self.assertEqual(creator, kwargs['creator'],
                         'creator search term should be included in solr query terms')
        self.assertEqual(creator, response.context['search_info']['creator'],
                         'creator search term should be included in search info for display to user')        

        # search by numbering scheme
        collection = FedoraFixtures.archives()[1]
        with patch('keep.collection.models.CollectionObject.find_by_pid',
                   new=Mock(return_value={'title': collection.label, 'pid': collection.pid})):
            response = self.client.get(search_url, {'collection-archive_id': collection.uri })
            args, kwargs = mocksunburnt.SolrInterface.return_value.query.call_args
            self.assertEqual(collection.uri, kwargs['archive_id'],
                'selected archive_id should be included in solr query terms')
            self.assertEqual(collection.pid, response.context['search_info']['Archive']['pid'],
                'archive label should be included in search info for display to user')        

        # shortcut to set the solr return value
        # NOTE: call order here has to match the way methods are called in view
        solrquery =  mocksunburnt.SolrInterface.return_value.query.return_value.sort_by.return_value
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

    @patch('keep.collection.views.sunburnt')
    def test_browse(self, mocksunburnt):
        browse_url = reverse('collection:browse')

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # shortcut to set the solr return value
        # NOTE: call order here has to match the way methods are called in view
        solrquery =  mocksunburnt.SolrInterface.return_value.query.return_value.sort_by.return_value
        solr_exec = solrquery.paginate.return_value.execute
        
        # no match
        # - set mock solr to return an empty result list
	solr_exec.return_value = [
            {'pid': 'pid:1', 'title': 'foo', 'source_id': 10,  'collection_label': 'marbl-coll'},
            {'pid': 'pid:2', 'title': 'bar', 'collection_label': 'marbl-coll'},
            {'pid': 'pid:3', 'title': 'baz', 'collection_label': 'pitts-coll'},
            {'pid': 'pid:4', 'title': '', 'collection_label': 'archives-coll'},
        ]

        default_search_args = {
            'pid': '%s:*' % settings.FEDORA_PIDSPACE,
            'content_model': CollectionObject.COLLECTION_CONTENT_MODEL,
        }
        response = self.client.get(browse_url)
        self.assertEqual(solr_exec.return_value, response.context['collections'],
            'solr result should be set as collections set in response context')
        args, kwargs = mocksunburnt.SolrInterface.return_value.query.call_args
        self.assertEqual('%s:*' % settings.FEDORA_PIDSPACE, kwargs['pid'],
                         'solr collection browse should be filtered by configured pidspace in solr query')
        self.assertEqual(CollectionObject.COLLECTION_CONTENT_MODEL, kwargs['content_model'],
                         'solr collection browse should be filtered by collection content model in solr query')
        solr_sort = mocksunburnt.SolrInterface.return_value.query.return_value.sort_by
        # solr query should be sorted on source id
        solr_sort.assert_called_with('source_id')

        # basic display checking
        
        # top-level collection object labels should display once for
        # each group, no matter how many items in the group
        self.assertContains(response, 'marbl-coll', 1,
            msg_prefix='collection label should be displayed once for each group, no matter how many items')
        self.assertContains(response, 'pitts-coll', 1,
            msg_prefix='collection label should be displayed once for each group, no matter how many items')
        self.assertContains(response, 'archives-coll', 1,
            msg_prefix='collection label should be displayed once for each group, no matter how many items')

        # item display
        self.assertContains(response, solr_exec.return_value[0]['title'],
            msg_prefix='result title should be included in the browse page')
        self.assertContains(response, solr_exec.return_value[0]['pid'],
            msg_prefix='result pid should be included in the browse page')
        self.assertContains(response, solr_exec.return_value[0]['source_id'],
            msg_prefix='result source id should be included in the browse page')
        
        # no title - default text
        self.assertContains(response, '(no title present)',
            msg_prefix='when a collection has no title, default no-title text is displayed')

        # test errors?

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


class SimpleCollectionTest( KeepTestCase):
    def setUp(self):
        self.repo = Repository()
        self.pids = []

        #Create fixtures and add to pid list
        self.simple_collection_1  = FedoraFixtures.simple_collection(label='Test Simple Collection 1', status='Processed')
        self.simple_collection_1.save()
        self.pids.append(self. simple_collection_1.pid)

        self.simple_collection_2  = FedoraFixtures.simple_collection(label='Test Simple Collection 2', status='Accessioned')
        self. simple_collection_2.save()
        self.pids.append(self.simple_collection_2.pid)

    def tearDown(self):
        for pid in self.pids:
            self.repo.purge_object(pid)

            

    def test_creation(self):
        obj = self.repo.get_object(type = SimpleCollection)
        obj.mods.content.create_restrictions_on_access()
        obj.mods.content.restrictions_on_access.text = 'processed'
        saved = obj.save()
        pid = obj.pid
        self.pids.append(pid)

        self.assertTrue(saved)
        self.assertEqual(obj. COLLECTION_CONTENT_MODEL, 'info:fedora/emory-control:Collection-1.0')
        self.assertEqual(obj.mods.content.restrictions_on_access.text, 'processed')
        
        self.assertTrue((obj.uriref, RDF.type, REPO.SimpleCollection) in obj.rels_ext.content,
                        'The collection is of type SimpleCollection')


    def test__objects_by_type(self):
        #Test Simple collection
        objs = _objects_by_type(REPO.SimpleCollection, SimpleCollection)
        obj_list = list(objs)
        self.assertTrue(len(obj_list) == 2)
        self.assertTrue(isinstance(obj_list[0], SimpleCollection), "object is of type SimpleCollection")

        #Test Simple collection wtith no obj type
        objs = _objects_by_type(REPO.SimpleCollection)
        obj_list = list(objs)
        self.assertTrue(len(obj_list) == 2)
        self.assertTrue(isinstance(obj_list[0], DigitalObject), "object is of type DigitalObject")

        #Test invalid type
        objs = _objects_by_type(REPO.FakeType)
        obj_list = list(objs)
        self.assertTrue(len(obj_list) == 0)

        
    def test_edit(self):
        edit_url = reverse('collection:simple_edit', kwargs={'pid' : self.simple_collection_2.pid})
        response = self.client.get(edit_url)
        expected, code = 200, response.status_code
        self.assertEqual(code, expected, 'Expected %s but returned %s' % (expected, code))

        self.assertContains(response, self.simple_collection_2.label)
        self.assertContains(response, 'Accessioned', msg_prefix='Status of collection should be Accessioned')

    def test_browse(self):
        browse_url = reverse('collection:simple_browse')
        response = self.client.get(browse_url)
        expected, code = 200, response.status_code
        self.assertEqual(code, expected, 'Expected %s but returned %s' % (expected, code))

        self.assertContains(response, self.simple_collection_1.label)
        self.assertContains(response, self.simple_collection_1.pid)
        self.assertContains(response, self.simple_collection_2.label)
        self.assertContains(response, self.simple_collection_2.pid)


class TestSimpleCollectionForm(KeepTestCase):
    def setUp(self):
        self.repo = Repository()
        self.pids = []

        #create ArrengementObject and associate to a collection
        #TODO Shold this be in arrangement app tests??
        self.arrangement_1 = self.repo.get_object(type= ArrangementObject)
        self.arrangement_1.label = "Test Arrangement Object 1"
        self.arrangement_1.state='I'
        self.arrangement_1.save()
        self.pids.append(self.arrangement_1.pid)

        self.arrangement_2 = self.repo.get_object(type= ArrangementObject)
        self.arrangement_2.label = "Test Arrangement Object 2"
        self.arrangement_2.state='I'
        self.arrangement_2.save()
        self.pids.append(self.arrangement_2.pid)

        #Create fixtures and add to pid list
        self.simple_collection_1  = FedoraFixtures.simple_collection(label='Test Simple Collection 1', status='Processed')
        self.simple_collection_1.save()
        self.pids.append(self.simple_collection_1.pid)

        self.simple_collection_2  = FedoraFixtures.simple_collection(label='Test Simple Collection 2', status='Accessioned')
        #add arrangements to collection
        self.simple_collection_2.rels_ext.content.add((self.simple_collection_2.uriref, relsext.hasMember, self.arrangement_1.uriref))
        self.simple_collection_2.rels_ext.content.add((self.simple_collection_2.uriref, relsext.hasMember, self.arrangement_2.uriref))
        self. simple_collection_2.save()
        self.pids.append(self.simple_collection_2.pid)


    def tearDown(self):
        for pid in self.pids:
            self.repo.purge_object(pid)

    def test_initial_data(self):
        form = cforms.SimpleCollectionEditForm(instance=self.simple_collection_2)

        #check label is set correctly
        self.assertEqual(form.object_instance.label, self.simple_collection_2.label)

        #check that restrictions_on_access_are set correctly
        self.assertEqual(form.object_instance.mods.content.restrictions_on_access.text,
                         self.simple_collection_2.mods.content.restrictions_on_access.text)

    def test_update_objects(self):
        #Change all the associated object statuses to 'A'
        form = cforms.SimpleCollectionEditForm(instance=self.simple_collection_2)

        (success, fail) = form.update_objects('Processed')
        self.assertEqual(success, 2)
        self.assertEqual(fail, 0)
        self.assertEqual(self.repo.get_object(pid=self.arrangement_1.pid, type=ArrangementObject).state, 'A')
        self.assertEqual(self.repo.get_object(pid=self.arrangement_2.pid, type=ArrangementObject).state, 'A')

        (success, fail) = form.update_objects('Accessioned')
        self.assertEqual(success, 2)
        self.assertEqual(fail, 0)
        self.assertEqual(self.repo.get_object(pid=self.arrangement_1.pid, type=ArrangementObject).state, 'I')
        self.assertEqual(self.repo.get_object(pid=self.arrangement_2.pid, type=ArrangementObject).state, 'I')


        #when bad status is given, nothing should change
        (success, fail) = form.update_objects('badstatus')
        self.assertEqual(success, 0)
        self.assertEqual(fail, 0)
        self.assertEqual(self.repo.get_object(pid=self.arrangement_1.pid, type=ArrangementObject).state, 'I')
        self.assertEqual(self.repo.get_object(pid=self.arrangement_2.pid, type=ArrangementObject).state, 'I')




