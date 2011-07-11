from django.core.urlresolvers import reverse
from django.test import Client

from keep.accounts.views import encrypt, decrypt, to_blocksize
# import encryption algorithm from views in case we ever want to change it
from keep.accounts.views import EncryptionAlgorithm
from keep.audio.tests import ADMIN_CREDENTIALS
from keep.testutil import KeepTestCase

class AccountViewsTest(KeepTestCase):
    fixtures =  ['users']
    
    def setUp(self):
        super(AccountViewsTest, self).setUp()
        self.client = Client()

    def test_to_blocksize(self):
        def test_valid_blocksize(text):
            block = to_blocksize(text)
            self.assertEqual(0, len(block) % EncryptionAlgorithm.block_size,
                '''text '%s' has correct block size for encryption algorithm''' % block)
            self.assert_(text in block, 'block-sized text contains original text')

        # test text of several sizes
        test_valid_blocksize('text')
        test_valid_blocksize('texty')
        test_valid_blocksize('textish')
        test_valid_blocksize('this is some text')
        test_valid_blocksize('this would be a really long password')
        test_valid_blocksize('can you imagine typing this every time you logged in?')

    def test_encrypt_decrypt(self):
        def test_encrypt_decrypt(text):
            encrypted = encrypt(text)
            self.assertNotEqual(text, encrypted,
                "encrypted text (%s) should not match original (%s)" % (encrypted, text))
            decrypted = decrypt(encrypted)
            self.assertEqual(text, decrypted,
                "decrypted text (%s) should match original encrypted text (%s)" % (decrypted, text))

        test_encrypt_decrypt('text')
        test_encrypt_decrypt('texty')
        test_encrypt_decrypt('textier')
        test_encrypt_decrypt('textiest')
        test_encrypt_decrypt('longish password-type text')

    def test_login(self):
        login_url = reverse('accounts:login')        
        # only testing custom logic, which happens on POST
        # everything else is handled by django.contrib.auth

        # failed login
        self.client.post(login_url, {'username':'fred', 'password': 'bogus'})
        self.assert_('fedora_password' not in self.client.session,
            'user password for fedora is not stored in session on failed login')

        # successful login
        self.client.post(login_url, ADMIN_CREDENTIALS)
        self.assert_('fedora_password' in self.client.session,
            'user password for fedora is stored in sesson on successful login')
        self.assertEqual(ADMIN_CREDENTIALS['password'],
            decrypt(self.client.session['fedora_password']),
            'user password stored in session is encrypted')

    def test_logout(self):
        index_url = reverse('audio:index')
        logout_url = reverse('accounts:logout')

        self.client.login(**ADMIN_CREDENTIALS)
        response = self.client.get(index_url)
        self.assertContains(response, logout_url,
            msg_prefix='when a user is logged in, response page should include logout url')

        response = self.client.get(logout_url, follow=True)
        self.assertNotContains(response, logout_url,
            msg_prefix='when a user is not logged in, response page should not include logout url')
