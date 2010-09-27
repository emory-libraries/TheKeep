import os
import urlparse
from rdflib import URIRef

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from eulcore.django.fedora.server import Repository
from eulcore.xmlmap  import load_xmlobject_from_string

from digitalmasters.audio import forms as audioforms
from digitalmasters.audio.models import AudioObject, Mods, ModsNote, ModsOriginInfo, \
        ModsDate, ModsIdentifier, ModsName, ModsNamePart, ModsRole, ModsAccessCondition, \
        ModsRelatedItem, CollectionObject, CollectionMods
from digitalmasters.audio.fixtures import FedoraFixtures

# NOTE: this user must be defined as a fedora user for certain tests to work
ADMIN_CREDENTIALS = {'username': 'euterpe', 'password': 'digitaldelight'}

# sample POST data for creating a collection
COLLECTION_DATA = {
    'title': 'Rushdie papers',
    'source_id': 'MSS1000',
    'date_created': '1947',
    'date_end': '2008',
    'collection': 'info:fedora/euterpe:marbl-archives',
    'resource_type': 'mixed material',
    'use_and_reproduction-text': 'no photos',
    'restrictions_on_access-text': 'tuesdays only',
    'name-type': 'personal',
    'name-authority': 'local',
    # 'management' form data is required for django to process formsets
    'name_parts-INITIAL_FORMS': '0',
    'name_parts-TOTAL_FORMS': '1',
    'name_parts-MAX_NUM_FORMS': '',
    'name_parts-0-text':'Mr. So and So',
    'roles-TOTAL_FORMS': '1',
    'roles-INITIAL_FORMS': '0',
    'roles-MAX_NUM_FORMS': '',
    'roles-0-authority': 'local',
    'roles-0-type': 'text',
    'roles-0-text': 'curator',
}

class AudioViewsTest(TestCase):
    fixtures =  ['users']

    def setUp(self):
        self.client = Client()

    def test_index(self):
        # test audio app index page permissions
        audio_index = reverse('audio:index')

        # not logged in
        response = self.client.get(audio_index)
        code = response.status_code
        expected = 302
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as AnonymousUser'
                             % (expected, code, audio_index))

        # logged in as staff
        self.client.login(**ADMIN_CREDENTIALS)
        response = self.client.get(audio_index)
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, audio_index))

        self.assert_(isinstance(response.context['search'], audioforms.SearchForm))
        self.assertContains(response, '<input')
        self.assertContains(response, 'Pid:')
        self.assertContains(response, 'Title:')

    def test_upload(self):
        # test upload form
        upload_url = reverse('audio:upload')

        # logged in as staff
        self.client.login(**ADMIN_CREDENTIALS)
        response = self.client.get(upload_url)
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, upload_url))

        self.assert_(isinstance(response.context['form'], audioforms.UploadForm))
        self.assertContains(response, 'Audio file')
        self.assertContains(response, '<input')

        # POST non-wav file results in an error
        f = open(os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.mp3'))
        response = self.client.post(upload_url, {'label': 'sample non-WAV', 'audio': f})
        # should only be one message
        for msg in response.context['messages']:
            self.assertEqual('Upload file must be a WAV file (got audio/mpeg)', str(msg))
            self.assertEqual('error', msg.tags)
        f.close()

        # POST actual wav file - no error
        f = open(os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.wav'))
        response = self.client.post(upload_url, {'label': 'sample WAV', 'audio': f}, follow=True)
        for msg in response.context['messages']:
            self.assert_('Successfully ingested WAV file' in str(msg))
            self.assertEqual('success', msg.tags)        
        f.close()

    def test_search(self):
        search_url = reverse('audio:search')

        # create some test objects to search for
        repo = Repository()
        obj = repo.get_object()
        obj.dc.content.title = "test search object 1"
        obj.save()
        obj2 = repo.get_object()
        obj2.dc.content.title = "test search object 2"
        obj2.save()

        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # search by exact pid
        response = self.client.get(search_url, {'pid': obj.pid})
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, search_url))
        self.assertContains(response, obj.pid,
                msg_prefix="test object 1 listed in results when searching by pid")
        self.assertNotContains(response, obj2.pid,
                msg_prefix="test object 2 not listed in results when searching by pid for test object 1")

        # search by title phrase
        response = self.client.get(search_url,
            {'title': 'test search', 'pid': '%s:' % settings.FEDORA_PIDSPACE })
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, search_url))
        self.assertContains(response, obj.pid,
                msg_prefix="test object 1 listed in results when searching by title")
        self.assertContains(response, obj2.pid,
                msg_prefix="test object 2 listed in results when searching by title")

        download_url = reverse('audio:download-audio', args=[obj.pid])
        self.assertContains(response, download_url,
                msg_prefix="search results link to audio download")

    def test_download_audio(self):
        # create a test audio object
        repo = Repository()
        obj = repo.get_object(type=AudioObject)
        obj.label = "my audio test object"
        obj.audio.content = open(os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.wav'))
        obj.save()
        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        download_url = reverse('audio:download-audio', args=[obj.pid])
        
        response = self.client.get(download_url)
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, download_url))
                             
        expected = 'audio/x-wav'
        self.assertEqual(response['Content-Type'], expected,
                        "Expected '%s' but returned '%s' for %s mimetype" % \
                        (expected, response['Content-Type'], download_url))
                        
        expected = 'attachment; filename=my-audio-test-object.wav'
        self.assertEqual(response['Content-Disposition'], expected,
                        "Expected '%s' but returned '%s' for %s content disposition" % \
                        (expected, response['Content-Type'], download_url))

    # NOTE: prototype edit form tests are failing; disabling because it's a *prototype*
    def disabled_test_edit(self):
        # create a test audio object to edit
        repo = Repository()
        obj = repo.get_object(type=AudioObject)
        obj.label = "my audio test object"
        obj.audio.content = open(os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.wav'))
        obj.save()
        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        edit_url = reverse('audio:edit', args=[obj.pid])

        response = self.client.get(edit_url)
        expected, code = 200, response.status_code
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, edit_url))
        self.assert_(isinstance(response.context['form'], audioforms.EditForm),
                "MODS EditForm is set in response context")
        self.assert_(isinstance(response.context['form'].instance, Mods),
                "form instance is a MODS xmlobject")

        # POST data to update MODS in fedora
        mods_data = {'title': 'new title',
                    'resource_type': 'text',
                    'note-label' : 'a general note',
                    'note-type': 'general',
                    'note-text': 'remember to ...',
                    'created-key_date': True,
                    'created-date': '2010-01-02',
                    }
        response = self.client.post(edit_url, mods_data, follow=True)
        messages = [ str(msg) for msg in response.context['messages'] ]
        self.assertEqual("Updated MODS for %s" % obj.pid, messages[0],
            "successful save message set in response context")
        # currently redirects to audio index
        (redirect_url, code) = response.redirect_chain[0]
        self.assert_(reverse('audio:index') in redirect_url,
            "attempting to edit non-existent pid redirects to audio index page")
        expected = 302      # redirect  -- maybe this should be a 303?
        self.assertEqual(code, expected,
            'Expected %s but returned %s for %s (edit non-existent record)'  % \
            (expected, code, edit_url))

        # retrieve the modified object from Fedora to check for updates
        updated_obj = repo.get_object(pid=obj.pid, type=AudioObject)
        self.assertEqual(mods_data['title'], updated_obj.mods.content.title,
            'mods title in fedora matches posted title')
        self.assertEqual(mods_data['resource_type'], updated_obj.mods.content.resource_type,
            'mods resource type in fedora matches posted resource type')
        self.assertEqual(mods_data['note-label'], updated_obj.mods.content.note.label,
            'mods note label in fedora matches posted note label')
        self.assertEqual(mods_data['note-type'], updated_obj.mods.content.note.type,
            'mods note type in fedora matches posted note type')
        self.assertEqual(mods_data['note-text'], updated_obj.mods.content.note.text,
            'mods note text in fedora matches posted note text')
        self.assertEqual(mods_data['created-key_date'],
            updated_obj.mods.content.origin_info.created.key_date,
            'mods created key date in fedora matches posted created key date')
        self.assertEqual(mods_data['created-date'],
            updated_obj.mods.content.origin_info.created.date,
            'mods created date in fedora matches posted created date')

        # force a schema-validation error (shouldn't happen normally)
        obj.mods.content = load_xmlobject_from_string(TestMods.invalid_xml, Mods)
        obj.save("schema-invalid MODS")
        response = self.client.post(edit_url, mods_data)

        self.assertContains(response, '<ul class="errorlist">')

        # edit non-existent record - exception
        fakepid = 'bogus-pid:1'
        edit_url = reverse('audio:edit', args=[fakepid])
        response = self.client.get(edit_url, follow=True)  # follow redirect to check error message
        messages = [ str(msg) for msg in response.context['messages'] ]
        self.assertEqual("Error: failed to load %s MODS for editing" % fakepid, messages[0],
            "load error message set in context when attempting to edit a non-existent pid")
        # currently redirects to audio index 
        (redirect_url, code) = response.redirect_chain[0]
        self.assert_(reverse('audio:index') in redirect_url,
            "attempting to edit non-existent pid redirects to audio index page")
        expected = 302      # redirect  -- maybe this should be a 303?
        self.assertEqual(code, expected,
            'Expected %s but returned %s for %s (edit non-existent record)'  % (expected, code, edit_url))


    def test_create_collection(self):
        # test creating a collection object
        # log in as staff
        # NOTE: using admin view so user credentials will be used to access fedora
        self.client.post(settings.LOGIN_URL, ADMIN_CREDENTIALS)

        new_coll_url = reverse('audio:new-collection')

        response = self.client.get(new_coll_url)
        expected, code = 200, response.status_code
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, new_coll_url))
        self.assert_(isinstance(response.context['form'], audioforms.CollectionForm),
                "MODS CollectionForm is set in response context")

        
        # test submitting incomplete/invalid data - should redisplay form with errors
        bad_data = COLLECTION_DATA.copy()
        del(bad_data['source_id'])
        del(bad_data['resource_type'])
        bad_data['collection'] = 'bogus-pid:123'
        response = self.client.post(new_coll_url, bad_data)
        self.assert_(isinstance(response.context['form'], audioforms.CollectionForm),
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
                      URIRef(CollectionObject.MEMBER_OF_COLLECTION),
                      URIRef(COLLECTION_DATA['collection'])) in
                      new_coll.rels_ext.content,
                      "collection object is member of requested top-level collection")

        # confirm that current site user appears in fedora audit trail
        xml, uri = new_coll.api.getObjectXML(new_coll.pid)
        self.assert_('<audit:responsibility>%s</audit:responsibility>' % ADMIN_CREDENTIALS['username'] in xml)


    def test_edit_collection(self):
        repo = Repository()
        obj = FedoraFixtures.rushdie_collection()
        # store initial collection id from fixture
        collection_uri = obj.collection_id
        obj.save()  # save to fedora for editing
        
        # log in as staff
        # NOTE: using admin view so user credentials will be used to access fedora
        self.client.post(settings.LOGIN_URL, ADMIN_CREDENTIALS)
        edit_url = reverse('audio:edit-collection', args=[obj.pid])

        response = self.client.get(edit_url)
        expected, code = 200, response.status_code
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, edit_url))
        self.assert_(isinstance(response.context['form'], audioforms.CollectionForm),
                "MODS CollectionForm is set in response context")
        self.assert_(isinstance(response.context['form'].instance, CollectionMods),
                "form instance is a collection MODS XmlObject")
        self.assertContains(response, 'value="MSS1000"',
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
        self.assert_(isinstance(response.context['form'], audioforms.CollectionForm),
                "MODS CollectionForm is set in response context after save and continue editing")

        # attempt to edit non-existent record
        edit_url = reverse('audio:edit-collection', args=['my-bogus-pid:123'])
        response = self.client.get(edit_url)
        expected, code = 404, response.status_code
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s (non-existing pid)'
                             % (expected, code, edit_url))

        # clean up - remove test object
        repo.purge_object(obj.pid, "removing unit test object")

    def test_collection_search(self):
        search_url = reverse('audio:search-collections')

        # ingest some test objects to search for
        repo = Repository()
        rushdie = FedoraFixtures.rushdie_collection()
        rushdie.save()  # save to fedora for searching
        esterbrook = FedoraFixtures.esterbrook_collection()
        esterbrook.save()
        engdocs = FedoraFixtures.englishdocs_collection()
        engdocs.save()
        pids = [rushdie.pid, esterbrook.pid, engdocs.pid]
        
        # log in as staff
        self.client.login(**ADMIN_CREDENTIALS)

        # search by MSS #
        response = self.client.get(search_url, {'mss': 'MSS1000'})
        self.assertContains(response, rushdie.pid,
                msg_prefix="Rushdie test collection object found when searching by Rushdie MSS #")
        self.assertNotContains(response, esterbrook.pid,
                msg_prefix="Esterbrook collection object not found when searching by Rushdie MSS #")

        # search by title phrase
        response = self.client.get(search_url, {'title': 'collection'})
        self.assertContains(response, rushdie.pid,
                msg_prefix="Rushdie collection found for title contains 'collection'")
        self.assertContains(response, engdocs.pid,
                msg_prefix="English Documents collection found for title contains 'collection'")
        self.assertNotContains(response, esterbrook.pid,
                msg_prefix="Esterbrook not found when searching for title contains 'collection'")
                
        # search by creator
        response = self.client.get(search_url, {'creator': 'esterbrook'})
        self.assertNotContains(response, rushdie.pid,
                msg_prefix="Rushdie collection not found for creator 'esterbrook'")
        self.assertContains(response, esterbrook.pid,
                msg_prefix="Esterbrook found when searching for creator 'esterbrook'")

        # search by collection
        collection = FedoraFixtures.top_level_collections[1].uri
        response = self.client.get(search_url, {'collection': collection })
        self.assertContains(response, rushdie.pid,
                msg_prefix="Rushdie collection found for collection %s" % collection)
        self.assertNotContains(response, esterbrook.pid,
                msg_prefix="Esterbrook not found when searching for collection %s" % collection)
        self.assertContains(response, engdocs.pid,
                msg_prefix="English Documents collection found for collection %s" % collection)

        # no match
        response = self.client.get(search_url, {'title': 'not-a-collection' })
        self.assertContains(response, 'no results',
                msg_prefix='Message should be displayed to user when search finds no matches')

        # clean up
        for p in pids:
            repo.purge_object(p)

    def test_collection_browse(self):
        browse_url = reverse('audio:browse-collections')

        # ingest test objects to browse
        repo = Repository()
        rushdie = FedoraFixtures.rushdie_collection()
        rushdie.save()  # save to fedora for searching
        esterbrook = FedoraFixtures.esterbrook_collection()
        esterbrook.save()
        engdocs = FedoraFixtures.englishdocs_collection()
        engdocs.save()
        pids = [rushdie.pid, esterbrook.pid, engdocs.pid]

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
            self.assertContains(response, obj.mods.content.source_id,
                msg_prefix="subcollection MSS # for %s is listed on collection browse page" % obj.pid)
            self.assertContains(response, unicode(obj.mods.content.name),
                msg_prefix="subcollection creator for %s is listed on collection browse page" % obj.pid)

        # test errors?

        # clean up
        for p in pids:
            repo.purge_object(p)


RealRepository = Repository
class FedoraCommsTest(TestCase):
    '''Test the app's response to fedora inaccessibility and unexpected
    fedora errors.'''

    fixtures =  ['users']

    def setUp(self):
        self.client = Client()
        self.client.login(**ADMIN_CREDENTIALS)

    def tearDown(self):
        self.restoreRepository()

    def useRepositoryRoot(self, root=None, host=None, port=None, path=None):
        if root is None:
            root = settings.FEDORA_ROOT
        root = self._update_root(root, host, port, path)

        # lots of Repository objects floating around here. let's do our
        # modules and namespacing very explicitly
        import eulcore.fedora.server
        import eulcore.django.fedora
        import eulcore.django.fedora.server
        import digitalmasters.audio.views

        username = getattr(settings, 'FEDORA_USER', None)
        password = getattr(settings, 'FEDORA_PASS', None)

        class RedirectedRepository(eulcore.fedora.server.Repository):
            def __init__(self, request=None):
                # take (and ignore) a request option to match local Repository class
                eulcore.fedora.server.Repository.__init__(self, root, username, password)
        if hasattr(settings, 'FEDORA_PIDSPACE'):
            RedirectedRepository.default_pidspace = settings.FEDORA_PIDSPACE

        eulcore.django.fedora.Repository = RedirectedRepository
        eulcore.django.fedora.server.Repository = RedirectedRepository
        digitalmasters.audio.views.Repository = RedirectedRepository

    def restoreRepository(self):
        import eulcore.django.fedora
        import eulcore.django.fedora.server
        import digitalmasters.audio.views
        eulcore.django.fedora.Repository = RealRepository
        eulcore.django.fedora.server.Repository = RealRepository
        digitalmasters.audio.views.Repository = RealRepository

    def _update_root(self, root, host, port, path):
        root_parts = urlparse.urlsplit(root)
        use_auth, at, hostport = root_parts.netloc.rpartition('@')
        use_host, colon, use_port = hostport.partition(':')
        use_parts = list(root_parts)

        if host is not None:
            use_host = host
        if port is not None:
            use_port = str(port)
            colon = ':' # just in case it wasn't already
        use_parts[1] = ''.join((use_auth, at, use_host, colon, use_port))

        if path is not None:
            use_parts[2] = path

        return urlparse.urlunsplit(use_parts)

    # _test not test so that this isn't picked up as a test case. this
    # method should be called from other test methods after changing the
    # repo root.
    def _testRepoErrors(self):
        # search
        url = reverse('audio:search')
        response = self.client.get(url, {'pid': 'fakepid:42'})
        self.assertContains(response, 'error contacting the digital repository',
                status_code=500)

        # upload
        url = reverse('audio:upload')
        f = open(os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.wav'))
        response = self.client.post(url, {'label': 'sample WAV', 'audio': f}) 
        self.assertContains(response, 'error contacting the digital repository',
                status_code=500)

        # edit

        # FIXME: this uses a different error reporting structure than the
        # other tests in this block. we should unify them. at the very
        # least, these errors should return 500, not 302.
        url = reverse('audio:edit', kwargs={'pid': 'fakepid:42'})
        response = self.client.get(url, follow=True)
        messages = [ str(msg) for msg in response.context['messages'] ]
        self.assertEqual("Error: failed to load fakepid:42 MODS for editing", messages[0],
            "load error message set in context when attempting to access bad fedora port")

        mods_data = {'title': 'new title',
                    'resource_type': 'text',
                    'note-label' : 'a general note',
                    'note-type': 'general',
                    'note-text': 'remember to ...',
                    'created-key_date': True,
                    'created-date': '2010-01-02',
                    }
        response = self.client.post(url, mods_data, follow=True)
        messages = [ str(msg) for msg in response.context['messages'] ]
        self.assertEqual("Error: failed to load fakepid:42 MODS for editing", messages[0],
            "load error message set in context when attempting to access bad fedora port")

        # download
        url = reverse('audio:download-audio', kwargs={'pid': 'fakepid:42'})
        response = self.client.get(url)
        self.assertContains(response, 'error contacting the digital repository',
                status_code=500)

    def testRepositoryDown(self):
        '''Verify we respond correctly when we can't connect to the repo.'''
        self.useRepositoryRoot(port=1)
        self._testRepoErrors()

    def testBadRepoUrl(self):
        '''Verify we respond correctly when the repo path is inaccessible.'''
        self.useRepositoryRoot(path='/')
        self._testRepoErrors()


# tests for (prototype) MODS XmlObject
class TestMods(TestCase):
    FIXTURE = """<mods:mods xmlns:mods="http://www.loc.gov/mods/v3">
  <mods:titleInfo>
    <mods:title>A simple record</mods:title>
  </mods:titleInfo>
  <mods:typeOfResource>text</mods:typeOfResource>
  <mods:note displayLabel="a general note" type="general">remember to...</mods:note>
  <mods:originInfo>
    <mods:dateCreated keyDate='yes'>2010-06-17</mods:dateCreated>
  </mods:originInfo>
  <mods:identifier type='uri'>http://so.me/uri</mods:identifier>
  <mods:name type="personal" authority="naf" ID="n82032703">
    <mods:namePart>Dawson, William Levi</mods:namePart>
    <mods:namePart type="date">1899-1990</mods:namePart>
    <mods:displayForm>William Levi Dawson (1899-1990)</mods:displayForm>
    <mods:affiliation>Tuskegee</mods:affiliation>
    <mods:role>
      <mods:roleTerm type="text" authority="marcrelator">Composer</mods:roleTerm>
    </mods:role>
  </mods:name>
  <mods:accessCondition type="restrictions on access">Restricted</mods:accessCondition>
  <mods:relatedItem type="host">
    <mods:titleInfo>
      <mods:title>Emory University Archives</mods:title>
    </mods:titleInfo>
  <mods:identifier type="local_sourcecoll_id">eua</mods:identifier>
  </mods:relatedItem>
</mods:mods>
"""
    invalid_xml = """<mods:mods xmlns:mods="http://www.loc.gov/mods/v3">
    <mods:titleInfo><mods:title invalid_attribute='oops'>An invalid record</mods:title></mods:titleInfo>
</mods:mods>
        """

    def setUp(self):
        self.mods = load_xmlobject_from_string(self.FIXTURE, Mods)

    def test_init_types(self):
        self.assert_(isinstance(self.mods, Mods))
        self.assert_(isinstance(self.mods.note, ModsNote))
        self.assert_(isinstance(self.mods.origin_info, ModsOriginInfo))
        self.assert_(isinstance(self.mods.origin_info.created[0], ModsDate))
        self.assert_(isinstance(self.mods.identifiers[0], ModsIdentifier))
        self.assert_(isinstance(self.mods.name, ModsName))
        self.assert_(isinstance(self.mods.name.name_parts[0], ModsNamePart))
        self.assert_(isinstance(self.mods.name.roles[0], ModsRole))
        self.assert_(isinstance(self.mods.access_conditions[0], ModsAccessCondition))
        self.assert_(isinstance(self.mods.related_items[0], ModsRelatedItem))

    def test_fields(self):
        self.assertEqual('A simple record', self.mods.title)
        self.assertEqual('text', self.mods.resource_type)
        self.assertEqual('a general note', self.mods.note.label)
        self.assertEqual('general', self.mods.note.type)
        self.assertEqual(u'remember to...', unicode(self.mods.note))
        self.assertEqual(u'2010-06-17', unicode(self.mods.origin_info.created[0]))
        self.assertEqual('2010-06-17', self.mods.origin_info.created[0].date)
        self.assertEqual(True, self.mods.origin_info.created[0].key_date)
        self.assertEqual(u'http://so.me/uri', self.mods.identifiers[0].text)
        self.assertEqual(u'uri', self.mods.identifiers[0].type)
        # name fields
        self.assertEqual(u'personal', self.mods.name.type)
        self.assertEqual(u'naf', self.mods.name.authority)
        self.assertEqual(u'n82032703', self.mods.name.id)
        self.assertEqual(u'Dawson, William Levi', self.mods.name.name_parts[0].text)
        self.assertEqual(u'1899-1990', self.mods.name.name_parts[1].text)
        self.assertEqual(u'date', self.mods.name.name_parts[1].type)
        self.assertEqual(u'William Levi Dawson (1899-1990)', self.mods.name.display_form)
        self.assertEqual(u'Tuskegee', self.mods.name.affiliation)
        self.assertEqual(u'text', self.mods.name.roles[0].type)
        self.assertEqual(u'marcrelator', self.mods.name.roles[0].authority)
        self.assertEqual(u'Composer', self.mods.name.roles[0].text)
        # access condition
        self.assertEqual(u'restrictions on access', self.mods.access_conditions[0].type)
        self.assertEqual(u'Restricted', self.mods.access_conditions[0].text)
        # related item
        self.assertEqual(u'host', self.mods.related_items[0].type)
        self.assertEqual(u'Emory University Archives', self.mods.related_items[0].title)
        self.assertEqual(u'local_sourcecoll_id', self.mods.related_items[0].identifiers[0].type)
        self.assertEqual(u'eua', self.mods.related_items[0].identifiers[0].text)

    def test_create_mods(self):
        # test creating MODS from scratch - ensure sub-xmlobject definitions are correct
        # and produce schema-valid MODS
        mods = Mods()
        mods.title = 'A Record'
        mods.resource_type = 'text'
        mods.name.type = 'personal'
        mods.name.authority = 'local'
        mods.name.name_parts.extend([ModsNamePart(type='family', text='Schmoe'),
                                    ModsNamePart(type='given', text='Joe')])
        mods.name.roles.append(ModsRole(type='text', authority='local',
                                        text='Test Subject'))
        mods.note.type = 'general'
        mods.note.text = 'general note'
        mods.origin_info.created.append(ModsDate(date='2001-10-02'))
        mods.record_id = 'id:1'
        mods.identifiers.extend([ModsIdentifier(type='uri', text='http://ur.l'),
                                 ModsIdentifier(type='local', text='332')])
        mods.access_conditions.extend([ModsAccessCondition(type='restriction', text='unavailable'),
                                       ModsAccessCondition(type='use', text='Tuesdays only')])
        mods.related_items.extend([ModsRelatedItem(type='host', title='EU Archives'),
                                   ModsRelatedItem(type='isReferencedBy', title='Finding Aid'),])
        xml = mods.serialize()
        self.assert_('<mods:mods ' in xml)
        self.assert_('xmlns:mods="http://www.loc.gov/mods/v3"' in xml)

        self.assertTrue(mods.is_valid(), "MODS created from scratch should be schema-valid")

    def test_isvalid(self):
        # if additions to MODS test fixture cause validation errors, uncomment the next 2 lines to debug
        #self.mods.is_valid()
        #print self.mods.validation_errors()
        self.assertTrue(self.mods.is_valid())        
        invalid_mods = load_xmlobject_from_string(self.invalid_xml, Mods)
        self.assertFalse(invalid_mods.is_valid())


# tests for (prototype) Audio DigitalObject
class TestAudioObject(TestCase):
    repo = Repository()

    def setUp(self):
        # create a test audio object to edit    
        self.obj = self.repo.get_object(type=AudioObject)
        self.obj.label = "Testing, one, two"
        self.obj.dc.content.title = self.obj.label
        self.obj.audio.content = open(os.path.join(settings.BASE_DIR, 'audio', 'fixtures', 'example.wav'))
        self.obj.save()

    def tearDown(self):
        self.repo.purge_object(self.obj.pid, "removing unit test fixture")

    def test_save(self):
        # save without changing the MODS - shouldn't mess anything up
        self.obj.save()
        self.assertEqual("Testing, one, two", self.obj.label)
        self.assertEqual("Testing, one, two", self.obj.dc.content.title)

        # set values in mods and save - should cascade to label, DC
        title, type, date = 'new title in mods', 'text', '2010-01-03'
        self.obj.mods.content.title = title
        self.obj.mods.content.resource_type = type
        self.obj.mods.content.origin_info.created.append(ModsDate(date=date))
        self.obj.save('testing custom save logic')

        # get updated copy from repo to check
        obj = self.repo.get_object(self.obj.pid, type=AudioObject)
        self.assertEqual(title, obj.label)
        self.assertEqual(title, obj.dc.content.title)
        self.assertEqual(type, obj.dc.content.type)
        self.assertEqual(date, obj.dc.content.date)


# tests for Collection DigitalObject
class TestCollectionObject(TestCase):
    repo = Repository()

    def test_top_level(self):
        collections = CollectionObject.top_level()
        self.assertEqual(3, len(collections),
                "top-level collection finds 3 items from fixture")
        self.assert_(isinstance(collections[0], CollectionObject),
                "top-level collection is instance of CollectionObject")
        # should this test pids from fixture?

    def test_collection_info(self):
        # test setting & getting collection membership
        repo = Repository()
        obj = repo.get_object(type=CollectionObject)
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
        repo = Repository()
        obj = repo.get_object(type=CollectionObject)
        # collection membership in RELS-EXT
        collections = CollectionObject.top_level()
        obj.set_collection(collections[0].uri)        
        obj.mods.content.source_id = 'MSS1000'
        obj.mods.content.title = 'Salman Rushdie Papers'
        obj.mods.content.resource_type = 'mixed material'
        # name
        obj.mods.content.name.name_parts.append(ModsNamePart(text='Salman Rushdie'))
        obj.mods.content.name.roles.append(ModsRole(text='author', authority='local'))
        # date range
        obj.mods.content.origin_info.created.append(ModsDate(date=1947, point='start'))
        obj.mods.content.origin_info.created.append(ModsDate(date=2008, point='end'))

        # update DC and check values
        obj._update_dc()
        self.assert_('MSS1000' in obj.dc.content.identifier_list,
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
        obj.mods.content.source_id = 'MSS123'
        obj.mods.content.title = 'Thomas Esterbrook letter books'
        obj.mods.content.resource_type = 'text'
        # name
        obj.mods.content.name.name_parts[0].text = 'Thomas Esterbrook'
        # single date
        obj.mods.content.origin_info.created.pop()  # remove second date
        obj.mods.content.origin_info.created[0].date = 1950
        obj.mods.content.origin_info.created[0].point = None

        obj._update_dc()
        self.assert_('MSS123' in obj.dc.content.identifier_list,
            'updated source identifier should be present in a dc:identifier')
        self.assert_('MSS1000' not in obj.dc.content.identifier_list,
            'previous source identifier should not be present in a dc:identifier')
        self.assertEqual(obj.mods.content.title, obj.dc.content.title,
            'dc:title should match updated title from MODS')
        self.assertEqual(obj.mods.content.resource_type, obj.dc.content.type,
            'dc:type should match updated resource type from MODS')
        self.assertEqual('Thomas Esterbrook', obj.dc.content.creator,
            'dc:creator set from updated MODS name')
        self.assertEqual('1950', obj.dc.content.date,
            'dc:date has single date from MODS')

    def test_subcollections(self):
         # ingest test collection objects
        repo = Repository()
        rushdie = FedoraFixtures.rushdie_collection()
        rushdie.save()
        esterbrook = FedoraFixtures.esterbrook_collection()
        esterbrook.save()
        engdocs = FedoraFixtures.englishdocs_collection()
        engdocs.save()
        pids = [rushdie.pid, esterbrook.pid, engdocs.pid]

        # rushdie & engdocs are in the same collection
        collection = repo.get_object(type=CollectionObject, pid=rushdie.collection_id)
        subcolls = collection.subcollections()
        self.assert_(isinstance(subcolls[0], CollectionObject),
            "subcollections methods returns instances of CollectionObject")
        subcoll_pids = [coll.pid for coll in subcolls]
        self.assert_(rushdie.pid in subcoll_pids,
            "rushdie should be included in subcollection for %s" % collection.pid)
        self.assert_(engdocs.pid in subcoll_pids,
            "engdocs should be included in subcollection for %s" % collection.pid)
        self.assert_(esterbrook.pid not in subcoll_pids,
            "esterbrook should be excluded from subcollections for %s" % collection.pid)

        # esterbrook is in a different collection
        collection = repo.get_object(type=CollectionObject, pid=esterbrook.collection_id)
        subcolls = collection.subcollections()
        subcoll_pids = [coll.pid for coll in subcolls]
        self.assert_(rushdie.pid not in subcoll_pids,
            "rushdie should be excluded from subcollections for %s" % collection.pid)
        self.assert_(engdocs.pid not in subcoll_pids,
            "engdocs should be excluded from subcollections for %s" % collection.pid)
        self.assert_(esterbrook.pid in subcoll_pids,
            "esterbrook should be included in subcollections for %s" % collection.pid)


        

        # clean up
        for p in pids:
            repo.purge_object(p)

class TestCollectionForm(TestCase):
    # test form data with all required fields
    data = COLLECTION_DATA

    def setUp(self):
        self.form = audioforms.CollectionForm(self.data)
        self.obj = FedoraFixtures.rushdie_collection()
        self.top_level_collections = FedoraFixtures.top_level_collections
        # store initial collection id from fixture
        self.collection_uri = self.obj.collection_id


    def test_subform_classes(self):
        # test that subforms are initialized with the correct classes
        sub = self.form.subforms['restrictions_on_access']
        self.assert_(isinstance(sub, audioforms.AccessConditionForm),
                    "restrictions on access subform should be instance of AccessConditionForm, got %s" \
                    % sub.__class__)
        sub = self.form.subforms['use_and_reproduction']
        self.assert_(isinstance(sub, audioforms.AccessConditionForm),
                    "use & reproduction subform should be instance of AccessConditionForm, got %s" \
                    % sub.__class__)
        sub = self.form.subforms['name']
        self.assert_(isinstance(sub, audioforms.NameForm),
                    "name subform should be instance of NameForm, got %s" % sub.__class__)
        fs = self.form.subforms['name'].formsets['name_parts'].forms[0]
        self.assert_(isinstance(fs, audioforms.NamePartForm),
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
        form = audioforms.CollectionForm(data)
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
        form = audioforms.CollectionForm(data, instance=self.obj)
        self.assertTrue(form.is_valid(), "test form object with test data is valid")
        form.update_instance()
        self.assertEqual(self.top_level_collections[2].uri, self.obj.collection_id)        

    def test_initial_data(self):
        form = audioforms.CollectionForm(instance=self.obj)
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