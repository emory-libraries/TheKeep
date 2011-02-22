from contextlib import contextmanager
from os import path

from rdflib import URIRef

from django.conf import settings
from django.core.urlresolvers import reverse, resolve
from django.test import Client, TestCase

from eulcore.django.test import TestCase as EulcoreTestCase
from eulcore.fedora.rdfns import relsext

from keep.collection.fixtures import FedoraFixtures 
from keep.collection import forms as cforms
from keep.collection import views
from keep.collection.models import CollectionObject, CollectionMods, FindingAid
from keep.common.fedora import Repository
from keep import mods

# NOTE: this user must be defined as a fedora user for certain tests to work
ADMIN_CREDENTIALS = {'username': 'euterpe', 'password': 'digitaldelight'}

# tests for Collection DigitalObject
class CollectionObjectTest(TestCase):
    repo = Repository()

    def test_top_level(self):
        collections = CollectionObject.top_level()
        self.assertEqual(3, len(collections),
                "top-level collection finds 3 items from fixture")
        self.assert_(isinstance(collections[0], CollectionObject),
                "top-level collection is instance of CollectionObject")
        # should this test pids from fixture?

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
        collections = CollectionObject.top_level()
        obj.set_collection(collections[0].uri)
        self.assertEqual(collections[0].uri, obj.collection_id)
        self.assertEqual(collections[0].label, obj.collection_label)

        # update collection membership
        obj.set_collection(collections[1].uri)
        self.assertEqual(collections[1].uri, obj.collection_id)
        self.assertEqual(collections[1].label, obj.collection_label)

    def test_update_dc(self):
        # DC should get updated from MODS & RELS-EXT on save

        # create test object and populate with data
        obj = self.repo.get_object(type=CollectionObject)
        # collection membership in RELS-EXT
        collections = CollectionObject.top_level()
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
        self.assertEqual(collections[0].uri, obj.dc.content.relation,
            'top-level collection URI set as dc:relation')
        # collection cmodel set as format (TEMPORARY)
        self.assertEqual(obj.COLLECTION_CONTENT_MODEL, obj.dc.content.format)

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

    def test_item_collections(self):
        pids = self.ingest_test_collections()

        with self.ingest_test_collections():
            collections = CollectionObject.item_collections()

            source_ids = [ coll['source_id']  for coll in collections ]
            self.assert_(1000 in source_ids,
                    "MSS# 1000 included in item collections")
            self.assert_(123 in source_ids,
                    "MSS# 123 included in item collections")
            self.assert_(309 in source_ids,
                    "MSS# 309 included in item collections")

            pids = [ coll['pid'] for coll in collections ]
            top_levels = CollectionObject.top_level()
            self.assert_(top_levels[0].pid not in pids,
                    "top level collection %s should not be in item collections." % (top_levels[0].pid,))

    def test_subcollections(self):
        with self.ingest_test_collections():
            # rushdie & engdocs are in the same collection
            collection = self.repo.get_object(type=CollectionObject, pid=self.rushdie.collection_id)            
            subcoll_pids = [coll['pid'] for coll in collection.subcollections()]
            self.assert_(self.rushdie.pid in subcoll_pids,
                "rushdie should be included in subcollection for %s" % collection.pid)
            self.assert_(self.engdocs.pid in subcoll_pids,
                "engdocs should be included in subcollection for %s" % collection.pid)
            self.assert_(self.esterbrook.pid not in subcoll_pids,
                "esterbrook should be excluded from subcollections for %s" % collection.pid)

            # esterbrook is in a different collection
            collection = self.repo.get_object(type=CollectionObject, pid=self.esterbrook.collection_id)
            subcolls = collection.subcollections()
            subcoll_pids = [coll['pid'] for coll in subcolls]
            self.assert_(self.rushdie.pid not in subcoll_pids,
                "rushdie should be excluded from subcollections for %s" % collection.pid)
            self.assert_(self.engdocs.pid not in subcoll_pids,
                "engdocs should be excluded from subcollections for %s" % collection.pid)
            self.assert_(self.esterbrook.pid in subcoll_pids,
                "esterbrook should be included in subcollections for %s" % collection.pid)


# sample POST data for creating a collection
COLLECTION_DATA = {
    'title': 'Rushdie papers',
    'source_id': '1000',
    'date_created': '1947',
    'date_end': '2008',
    'collection': 'info:fedora/keep:marbl',
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

class TestCollectionForm(TestCase):
    # test form data with all required fields
    data = COLLECTION_DATA

    def setUp(self):
        self.form = cforms.CollectionForm(self.data)
        self.obj = FedoraFixtures.rushdie_collection()
        self.top_level_collections = FedoraFixtures.top_level_collections
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
        data['collection'] = self.top_level_collections[2].uri
        form = cforms.CollectionForm(data, instance=self.obj)
        self.assertTrue(form.is_valid(), "test form object with test data is valid")
        form.update_instance()
        self.assertEqual(self.top_level_collections[2].uri, self.obj.collection_id)

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


class CollectionViewsTest(EulcoreTestCase):
    fixtures =  ['users']
    repo = Repository()

    def setUp(self):
        self.client = Client()
        self.pids = []

    def tearDown(self):
        # purge any objects created by individual tests
        for pid in self.pids:
            self.repo.purge_object(pid)

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
        response = self.client.post(new_coll_url, COLLECTION_DATA, follow=True)
        # do we need to test actual response, redirect ?
        messages = [ str(msg) for msg in response.context['messages'] ]
        self.assert_('Created new collection' in messages[0],
            'successful collection creation message displayed to user')
        # get pid of created object and inspect in fedora
        pid = messages[0].replace('Created new collection ', '')
        repo = Repository()
        new_coll = repo.get_object(pid, type=CollectionObject)
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

        # POST and update existing object, verify in fedora
        response = self.client.post(edit_url, COLLECTION_DATA, follow=True)
        messages = [ str(msg) for msg in response.context['messages'] ]
        self.assertEqual('Updated collection %s' % obj.pid, messages[0],
            'successful collection update message displayed to user')
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
        self.assertEqual('Updated collection %s' % obj.pid, messages[0],
            'successful collection update message displayed to user on save and continue editing')
        self.assert_(isinstance(response.context['form'], cforms.CollectionForm),
                "MODS CollectionForm is set in response context after save and continue editing")

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
        self.assertEqual(views.edit, view_func,
            'redirect url %s should resolve to edit_collection view' % redirect_url)
        self.assert_('pid' in kwargs, 'object pid is set in resolved url keyword args')

        messages = [ str(msg) for msg in response.context['messages'] ]
        self.assert_('Created new collection' in messages[0],
            'successful collection creation message displayed to user on save and continue editing')

        # attempt to edit non-existent record
        edit_url = reverse('collection:edit', args=['my-bogus-pid:123'])
        response = self.client.get(edit_url)
        expected, code = 404, response.status_code
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s (non-existing pid)'
                             % (expected, code, edit_url))

    def test_search(self):
        search_url = reverse('collection:search')

        # ingest some test objects to search for
        repo = Repository()
        rushdie = FedoraFixtures.rushdie_collection()
        rushdie.save()  # save to fedora for searching
        esterbrook = FedoraFixtures.esterbrook_collection()
        esterbrook.save()
        engdocs = FedoraFixtures.englishdocs_collection()
        engdocs.save()
        self.pids.extend([rushdie.pid, esterbrook.pid, engdocs.pid])

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # search by MSS #
        response = self.client.get(search_url, {'collection-mss': '1000'})
        found = [o['pid'] for o in response.context['results']]
        self.assert_(rushdie.pid in found,
                "Rushdie test collection object found when searching by Rushdie MSS #")
        self.assert_(esterbrook.pid not in found,
                "Esterbrook collection object not found when searching by Rushdie MSS #")
        self.assertPattern('Collection Number:.*1000', response.content,
            msg_prefix='search results page should include search term (MSS #)')

        # search by title phrase
        response = self.client.get(search_url, {'collection-title': 'collection'})
        found = [o['pid'] for o in response.context['results']]
        self.assert_(rushdie.pid in found,
                "Rushdie collection found for title contains 'collection'")
        self.assert_(engdocs.pid in found,
                "English Documents collection found for title contains 'collection'")
        self.assert_(esterbrook.pid not in found,
                "Esterbrook not found when searching for title contains 'collection'")
        self.assertPattern('title:.*collection', response.content,
            msg_prefix='search results page should include search term (title)')

        # search by creator
        response = self.client.get(search_url, {'collection-creator': 'esterbrook'})
        found = [o['pid'] for o in response.context['results']]
        self.assert_(rushdie.pid not in found,
                "Rushdie collection not found for creator 'esterbrook'")
        self.assert_(esterbrook.pid in found,
                "Esterbrook found when searching for creator 'esterbrook'")
        self.assertPattern('creator:.*esterbrook', response.content,
            msg_prefix='search results page should include search term (creator)')

        # search by numbering scheme
        collection = FedoraFixtures.top_level_collections[1]
        response = self.client.get(search_url, {'collection-collection': collection.uri })
        found = [o['pid'] for o in response.context['results']]
        self.assert_(rushdie.pid in found,
                "Rushdie collection found for collection %s" % collection.uri)
        self.assert_(esterbrook.pid not in found,
                "Esterbrook not found when searching for collection %s" % collection.uri)
        self.assert_(engdocs.pid in found,
                "English Documents collection found for collection %s" % collection.uri)
        self.assertPattern('Collection:.*%s' % collection.label, response.content,
            msg_prefix='search results page should include search term (numbering scheme)')

        # no match
        response = self.client.get(search_url, {'collection-title': 'not-a-collection' })
        self.assertContains(response, 'no results',
                msg_prefix='Message should be displayed to user when search finds no matches')


    def test_browse(self):
        browse_url = reverse('collection:browse')

        # ingest test objects to browse
        repo = Repository()
        rushdie = FedoraFixtures.rushdie_collection()
        rushdie.save()  # save to fedora for searching
        esterbrook = FedoraFixtures.esterbrook_collection()
        esterbrook.save()
        engdocs = FedoraFixtures.englishdocs_collection()
        engdocs.save()
        self.pids.extend([rushdie.pid, esterbrook.pid, engdocs.pid])

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        response = self.client.get(browse_url)
        self.assert_(response.context['collections'],
            'top-level collection object list is set in response context')
        for obj in FedoraFixtures.top_level_collections:
            self.assertContains(response, obj.label,
                msg_prefix="top-level collection %s is listed on collection browse page" % obj.label)

        for obj in rushdie, esterbrook, engdocs:
            self.assertContains(response, obj.mods.content.title,
                msg_prefix="subcollection title for %s is listed on collection browse page" % obj.pid)
            self.assertContains(response, str(obj.mods.content.source_id),
                msg_prefix="subcollection MSS # for %s is listed on collection browse page" % obj.pid)
            if obj.mods.content.name:
                self.assertContains(response, unicode(obj.mods.content.name),
                    msg_prefix="subcollection creator for %s is listed on collection browse page" % obj.pid)

        # test errors?



class FindingAidTest(EulcoreTestCase):
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

