import os

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from eulcore.django.fedora.server import Repository

from digitalmasters.audio.forms import UploadForm, SearchForm

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
        response = self.client.post(search_url, {'pid': obj.pid})
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, search_url))
        self.assertContains(response, obj.pid,
                msg_prefix="test object 1 listed in results when searching by pid")
        self.assertNotContains(response, obj2.pid,
                msg_prefix="test object 2 not listed in results when searching by pid for test object 1")

        # search by title phrase
        response = self.client.post(search_url,
            {'title': 'test search', 'pid': '%s:' % settings.FEDORA_PIDSPACE })
        code = response.status_code
        expected = 200
        self.assertEqual(code, expected, 'Expected %s but returned %s for %s as admin'
                             % (expected, code, search_url))
        self.assertContains(response, obj.pid,
                msg_prefix="test object 1 listed in results when searching by title")
        self.assertContains(response, obj2.pid,
                msg_prefix="test object 2 listed in results when searching by title")

        
        
        

        
        