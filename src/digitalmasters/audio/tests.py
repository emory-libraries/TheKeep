import os

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from eulcore.django.fedora.server import Repository
from eulcore.xmlmap  import load_xmlobject_from_string

from digitalmasters.audio.forms import UploadForm, SearchForm
from digitalmasters.audio.models import AudioObject, Mods, ModsNote, ModsOriginInfo, ModsDate

class AudioTest(TestCase):
    fixtures =  ['users']
    admin_credentials = {'username': 'euterpe', 'password': 'digitaldelight'}

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
        self.client.login(**self.admin_credentials)
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
        self.client.login(**self.admin_credentials)
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
        self.client.login(**self.admin_credentials)

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
        self.client.login(**self.admin_credentials)

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

        invalid = """<mods:mods xmlns:mods="http://www.loc.gov/mods/v3">
    <mods:titleInfo><mods:title invalid_attribute='oops'>An invalid record</mods:title></mods:titleInfo>
</mods:mods>
        """
        invalid_mods = load_xmlobject_from_string(invalid, Mods)
        self.assertFalse(invalid_mods.is_valid())
        
