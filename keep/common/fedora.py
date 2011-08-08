from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.encoding import iri_to_uri

from eulfedora import models, server
from eulxml import xmlmap
from pidservices.clients import parse_ark
from pidservices.djangowrapper.shortcuts import DjangoPidmanRestClient

from keep import mods
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


# keep-specific mods with common fields for all Keep objects
class LocalMODS(mods.MODS):
    # short-cut to type-specific identifiers
    ark = xmlmap.StringField('mods:identifier[@type="ark"]')
    ark_uri = xmlmap.StringField('mods:identifier[@type="uri"][contains(., "ark:")]')
    

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

    @property
    def default_owner(self):
        return getattr(settings, 'FEDORA_OBJECT_OWNERID', None)

    @property
    def default_pidspace(self):
        return getattr(settings, 'FEDORA_PIDSPACE', None)

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
        # Find the short-form ARK based on the ark_access_uri.

        # if we have access to mods with ark mapped, use that
        if hasattr(self, 'mods') and \
            hasattr(self.mods.content, 'ark'):
            return self.mods.content.ark
        
        # otherwise, calculate based on ark_access_uri
        if self.ark_access_uri is not None:
            idx = self.ark_access_uri.find('ark:')
            if idx < 0: # this would be an error in pidman-derived data
                return None
            return self.ark_access_uri[idx:]

    @property
    def ark_access_uri(self):
        # if we have a mods datastream, ARK should be set in mods:identifier
        if hasattr(self, 'mods'):
            # if mods has ark_uri mapped, use that
            if hasattr(self.mods.content, 'ark_uri'):
                return self.mods.content.ark_uri
            # otherwise, search by type and ark: text
            ark_uri = [id.text for id in self.mods.content.identifiers
                       if id.type == 'uri' and 'ark:' in id.text]
            if ark_uri:
                return ark_uri[0]

        # if we don't have mods, look for ark in dc:identifier
        else:
            ark_uri = [id for id in self.dc.content.identifier_list
                       if 'ark:' in id]
            if ark_uri:
                return ark_uri[0]

    @property
    def default_target_data(self):
        # get information about this ARK from the pid manager
        # (formerly used to determine ark_access_uri)
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
        '''Default pid logic for DigitalObjects in the Keep.  Mint a
        new ARK via the PID manager, store the ARK in the MODS
        metadata (if available) or Dublin Core, and use the noid
        portion of the ARK for a Fedora pid in the site-configured
        Fedora pidspace.'''
        
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
            # pid name is not required, but helpful for managing pids
            pid_name = self.label
            # ask pidman for a new ark in the configured pidman domain
            ark = pidman.create_ark(settings.PIDMAN_DOMAIN, target, name=pid_name)
            # pidman returns the full, resolvable ark
            # parse into dictionary with nma, naan, and noid
            parsed_ark = parse_ark(ark)
            naan = parsed_ark['naan']  # name authority number
            noid = parsed_ark['noid']  # nice opaque identifier

            # if we have a mods datastream, store the ARK as mods:identifier
            if hasattr(self, 'mods'):
                # store full uri and short-form ark
                self.mods.content.identifiers.extend([
                    mods.Identifier(type='ark', text='ark:/%s/%s' % (naan, noid)),
                    mods.Identifier(type='uri', text=ark)
                    ])
            else:
                # otherwise, add full uri ARK to dc:identifier
                self.dc.content.identifier_list.append(ark)
            
            # use the noid to construct a pid in the configured pidspace
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
                #username =request.user.username
                #password = decrypt(request.session['fedora_password'])
                username = 'fedoraAdmin'
                password = 'DietCoke55'        
        super(Repository, self).__init__(username=username, password=password)
