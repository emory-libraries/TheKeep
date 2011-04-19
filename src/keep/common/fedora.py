from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.encoding import iri_to_uri
from eulcore.fedora import models
from eulcore.django.fedora import server
from pidservices.djangowrapper.shortcuts import DjangoPidmanRestClient
from keep.accounts.views import decrypt
from keep.common.utils import absolutize_url

# TODO: write unit tests now that this code is an app and django knows how to run tests for it

# try to configure a pidman client to get pids.
try:
    pidman = DjangoPidmanRestClient()
except:
    # if we're in dev mode then we can fall back on the fedora default
    # pid allocator. in non-dev, though, we really need pidman
    if getattr(settings, 'DEV_ENV', False):
        pidman = None
    else:
        raise

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
    default_pidspace = getattr(settings, 'FEDORA_PIDSPACE', None)

    def __init__(self, *args, **kwargs):
        super(DigitalObject, self).__init__(*args, **kwargs)
        self._default_target_data = None

    def _init_as_new_object(self):
        super(DigitalObject, self)._init_as_new_object()

        if self.default_owner:
            self.info.owner = self.default_owner

    @property
    def noid(self):
        pidspace, noid = self.pid.split(':')
        return noid

    @property
    def ark(self):
        if self.ark_access_uri is not None:
            idx = self.ark_access_uri.find('ark:')
            if idx < 0: # this would be an error in pidman-derived data
                return None
            return self.ark_access_uri[idx:]

    @property
    def ark_access_uri(self):
        if self.default_target_data is not None:
            return self.default_target_data['access_uri']

    @property
    def default_target_data(self):
        if self._default_target_data is None:
            try:
                self._default_target_data = pidman.get_ark_target(self.noid, '')
                ark_data = pidman.get_ark(self.noid)
            except:
                return None
            ark_uri = ark_data['uri']
            default_target = ark_uri + '/'
            for target in ark_data['targets']:
                if target['uri'] == default_target:
                    self._default_target_data = target
                    break

        return self._default_target_data

    PID_TOKEN = '{%PID%}'
    ENCODED_PID_TOKEN = iri_to_uri(PID_TOKEN)
    def get_default_pid(self):
        if pidman is not None:
            # pidman wants a target for the new pid
            '''Get a pidman-ready target for a named view.'''

            # first just reverse the view name.
            pid = '%s:%s' % (self.default_pidspace, self.PID_TOKEN)
            target = reverse(self.NEW_OBJECT_VIEW, kwargs={'pid': pid})
            # reverse() encodes the PID_TOKEN, so unencode just that part
            target = target.replace(self.ENCODED_PID_TOKEN, self.PID_TOKEN)
            # reverse() returns a full path - absolutize so we get scheme & server also
            target = absolutize_url(target)
            # ask pidman for a new ark in the configured pidman domain
            ark = pidman.create_ark(settings.PIDMAN_DOMAIN, target)
            # grab the noid from the tail end of the ark
            arkbase, slash, noid = ark.rpartition('/')
            # and construct a pid in the configured pidspace
            return '%s:%s' % (self.default_pidspace, noid)
        else:
            # if pidmanager is not available, fall back to default pid behavior
            return super(DigitalObject, self).get_default_pid()
            


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
