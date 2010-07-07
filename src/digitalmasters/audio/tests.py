import os
import urlparse

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from eulcore.django.fedora.server import Repository
from eulcore.xmlmap  import load_xmlobject_from_string

from digitalmasters.audio.forms import UploadForm, SearchForm, EditForm
from digitalmasters.audio.models import AudioObject, Mods, ModsNote, ModsOriginInfo, ModsDate

ADMIN_CREDENTIALS = {'username': 'euterpe', 'password': 'digitaldelight'}

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

        self.assert_(isinstance(response.context['search'], SearchForm))
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

        self.assert_(isinstance(response.context['form'], UploadForm))
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
        obj.label = "test search object 1"
        obj.save()
        obj2 = repo.get_object()
        obj2.label = "test search object 2"
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
                             
    def test_edit(self):
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
        self.assert_(isinstance(response.context['form'], EditForm),
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
            def __init__(self):
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

    def testRepositoryDown(self):
        '''Verify we respond correctly when we can't connect to the repo.'''
        self.useRepositoryRoot(port=1)

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
        self.assert_(isinstance(self.mods.origin_info.created, ModsDate))

    def test_fields(self):
        self.assertEqual('A simple record', self.mods.title)
        self.assertEqual('text', self.mods.resource_type)
        self.assertEqual('a general note', self.mods.note.label)
        self.assertEqual('general', self.mods.note.type)
        self.assertEqual(u'remember to...', unicode(self.mods.note))
        self.assertEqual(u'2010-06-17', unicode(self.mods.origin_info.created))
        self.assertEqual('2010-06-17', self.mods.origin_info.created.date)
        self.assertEqual(True, self.mods.origin_info.created.key_date)   # oversimplifying boolean here

    def test_template_init(self):
        mods = Mods()
        xml = mods.serialize()
        self.assert_('<mods:mods ' in xml)
        self.assert_('xmlns:mods="http://www.loc.gov/mods/v3"' in xml)
        # TODO: can't yet create from scratch because fields are nested...

    def test_isvalid(self):
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
        self.obj.mods.content.origin_info.created.date = date
        self.obj.save('testing custom save logic')

        # get updated copy from repo to check
        obj = self.repo.get_object(self.obj.pid, type=AudioObject)
        self.assertEqual(title, obj.label)
        self.assertEqual(title, obj.dc.content.title)
        self.assertEqual(type, obj.dc.content.type)
        self.assertEqual(date, obj.dc.content.date)
