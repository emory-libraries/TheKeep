from django.test import Client, TestCase
from django.core.urlresolvers import reverse

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

        