from Crypto.Cipher import Blowfish as EncryptionAlgorithm
import hashlib
import logging

from django.conf import settings
from django.contrib.auth import views as authviews
from django.core.urlresolvers import reverse

from eulcommon.djangoextras.http import HttpResponseSeeOtherRedirect

logger = logging.getLogger(__name__)

def login(request):
    '''Custom login view.  Calls the standard Django authentication, but on
    successful login, stores encrypted user credentials in order to allow
    accessing the Fedora repository as the currently logged in user.
    '''
    response = authviews.login(request, 'accounts/login.html')
    if request.method == "POST" and request.user.is_authenticated():
        # on successful login, encrypt and store user's password to use for fedora access
        request.session['fedora_password'] = encrypt(request.POST.get('password'))

        next_url = request.POST.get('next', None)
        if request.user.is_authenticated() and not next_url and \
           request.user.is_staff:
            # if the user is staff, redirect to admin dashboard
            next_url = reverse('repo-admin:dashboard')
            return HttpResponseSeeOtherRedirect(next_url)

    return response

def logout(request):
    return authviews.logout(request, next_page=reverse('site-index'))

# NOTE: current encryption logic should be easily adapted to most of the
# encryption algorithms supported by Crypto that allow for variable key length

ENCRYPT_PAD_CHARACTER = '\0'
# NOTE: Blowfish key length is variable but must be 32-448 bits
# (but PyCrypto does not actually make this information accessible)
KEY_MIN_CHARS = 32/8
KEY_MAX_CHARS = 448/8
if KEY_MIN_CHARS <= len(settings.SECRET_KEY) <= KEY_MAX_CHARS:
    ENCRYPTION_KEY = settings.SECRET_KEY
else:
    ENCRYPTION_KEY = hashlib.sha224(settings.SECRET_KEY).hexdigest()
    message = '''Django secret key length (%d) requires hashing for use as encryption key
    (to avoid hashing, should be %d-%d characters)''' % \
        (len(settings.SECRET_KEY), KEY_MIN_CHARS, KEY_MAX_CHARS)
    logger.warn(message)

def encrypt(text):
    crypt = EncryptionAlgorithm.new(ENCRYPTION_KEY)
    return crypt.encrypt(to_blocksize(text))

def decrypt(text):
    crypt = EncryptionAlgorithm.new(ENCRYPTION_KEY)
    return crypt.decrypt(text).rstrip(ENCRYPT_PAD_CHARACTER)

def to_blocksize(password):
    # pad the text to create a string of acceptable block size for the encryption algorithm
    width = len(password) + \
        (EncryptionAlgorithm.block_size - len(password) % EncryptionAlgorithm.block_size)
    block = password.ljust(width, ENCRYPT_PAD_CHARACTER)
    return block

