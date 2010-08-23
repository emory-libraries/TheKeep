from Crypto.Cipher import Blowfish as EncryptionAlgorithm

from django.conf import settings
from django.contrib.auth import views as authviews

def login(request):
    response = authviews.login(request, 'accounts/login.html')
    if request.method == "POST" and request.user.is_authenticated():
        # on successful login, encrypt and store user's password to use for fedora access
        request.session['fedora_password'] = encrypt(request.POST.get('password'))
    return response

# NOTE: current encryption logic should work with most of the encryption algorithms
# supported by Crypto that allow for variable key length

ENCRYPT_PAD_CHARACTER = '\0'

def encrypt(text):
    crypt = EncryptionAlgorithm.new(settings.SECRET_KEY)
    return crypt.encrypt(to_blocksize(text))

def decrypt(text):
    crypt = EncryptionAlgorithm.new(settings.SECRET_KEY)
    return crypt.decrypt(text).rstrip(ENCRYPT_PAD_CHARACTER)

def to_blocksize(password):
    # pad the text to create a string of acceptable block size for the encryption algorithm
    width = len(password) + \
        (EncryptionAlgorithm.block_size - len(password) % EncryptionAlgorithm.block_size)
    block = password.ljust(width, ENCRYPT_PAD_CHARACTER)
    return block

