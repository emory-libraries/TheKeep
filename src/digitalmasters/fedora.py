from django.conf import settings
from eulcore.fedora import models
from eulcore.django.fedora import server
from digitalmasters.accounts.views import decrypt

class DigitalObject(models.DigitalObject):
    """Extend the default fedora DigitalObject class. Objects derived from
    this one will automatically have their owner set to
    ``settings.FEDORA_OBJECT_OWNERID``. This happens only when the fedora
    object is ingested, so it won't happen to objects already in the
    repository.

    As an implementation detail, we need this right now for security: Some
    of our security policies use the owner to identify objects associated
    with this project. We hope FeSL will enable us to get away from this
    practice, at which point this class will probably no longer be
    necessary."""

    default_owner = getattr(settings, 'FEDORA_OBJECT_OWNERID', None)

    def _init_as_new_object(self):
        super(DigitalObject, self)._init_as_new_object()

        if self.default_owner:
            self.info.owner = self.default_owner


class Repository(server.Repository):
    """Extend the Django-ized Fedora Repository object to take a request object
    and connect to Fedora using a user is logged in and the required credentials
    are available.  If no request is specified or no user is logged in, falls
    back to the default logic, which uses Django settings for Fedora credentials.
    """

    default_object_type = DigitalObject

    def __init__(self, username=None, password=None, request=None):        
        if request is not None and request.user.is_authenticated() and \
            'fedora_password' in request.session:            
                username =request.user.username
                password = decrypt(request.session['fedora_password'])            
        super(Repository, self).__init__(username=username, password=password)
