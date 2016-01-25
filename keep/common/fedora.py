from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render
import urllib

from eulfedora import models, server
from eulfedora.util import RequestFailed, PermissionDenied
from eulfedora.models import DublinCore, XmlDatastream, RdfDatastream
from eulxml import xmlmap
from eulxml.xmlmap import mods
from pidservices.clients import parse_ark
from pidservices.djangowrapper.shortcuts import DjangoPidmanRestClient

from keep.accounts.views import decrypt
from keep.common.utils import absolutize_url, solr_interface

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
class LocalMODS(xmlmap.mods.MODS):
    # short-cut to type-specific identifiers
    ark = xmlmap.StringField('mods:identifier[@type="ark"]')
    ark_uri = xmlmap.StringField('mods:identifier[@type="uri"][contains(., "ark:")]')



class AuditTrailEvent(object):
    '''An object to cluster a group of related Fedora
    :class:`~eulfedora.xml.AuditTrailRecord` objects into a single
    audit trail "event"; i.e., when a single edit form save updates
    multiple datastreams and makes multiple API calls.

    Initial arguments:

    :param record: optional :class:`~eulfedora.xml.AuditTrailRecord`,
      used to initialize values

    :param component_key: optional dictionary of human-readable names
      keyed on datastream ID (or
      :attr:`~eulfedora.xml.AuditTrailRecord.component` in the audit trail)
    '''

    date = None
    'approximate date for all records in this event'
    user = None
    'username for the user responsible for all API calls in this event'
    components = []
    'list of components modified by all API calls in this event'
    message = None
    'log message associated with all API calls in this event'
    actions = set()
    'uniqe set of all API actions included in this event'

    def __init__(self, record=None, component_key=None):
        self.components = []
        self.actions = set()
        if record:
            self.date = record.date
            self.user = record.user
            self.message = record.message
            if record.component:
                self.components = [record.component]
            self.actions = set([record.action])

        self.component_key = component_key

    def add_record(self, record):
        '''Add another :class:`~eulfedora.xml.AuditTrailRecord` to
        this events (updates actions and components as appropriate).

        :param record: :class:`~eulfedora.xml.AuditTrailRecord`
        '''
        self.date = record.date
        self.actions.add(str(record.action))
        # component could be empty for non-datastream based actions
        if record.component:
            self.components.append(record.component)

    def component_names(self):
        '''Return a list of human-readable names for the components
        modified by this event; requires component_key to be set when
        initialized.
        '''
        if self.component_key:
            return set([self.component_key[c] for c in self.components
                        if c in self.component_key])

    def user_name(self):
        '''Return the full name for the user responsible for this
        event, via :meth:`user_full_name`.
        '''
        return user_full_name(self.user)

    @property
    def action(self):
        '''Brief, summary action label for the audit trail records
        grouped in this event, e.g. ``modify`` or ``ingest``.
        '''
        if any(a.startswith('modify') for a in self.actions):
            return 'edit'
        elif self.actions:
            return list(self.actions)[0]


class DuplicateContent(Exception):
    '''Custom exception to prevent ingest when duplicate content is
    detected.  The optional list of pids should be specified when possible,
    to allow investigating the objects detected as duplicates; a pid to
    content model mapping should also provided if possible, to allow
    exception handling to detect the object type of the duplicate records.'''
    def __init__(self, message, pids=[], pid_cmodels={}):
        Exception.__init__(self, message)
        self.pids = pids
        self.pid_cmodels = pid_cmodels


class ArkPidDigitalObject(models.DigitalObject):
    """Default base fedora DigitalObject class for all :mod:`keep` objects,
    with functionalty shared across all Keep content.

    Objects derived from this one will automatically have their owner set to
    ``settings.FEDORA_OBJECT_OWNERID`` at ingest time (does not affect
    objects already in the repository). [Note that owner id is currently used
    for security purposes to identify Keep content in Fedora policies.]
    """

    dc = XmlDatastream("DC", "Dublin Core", DublinCore, defaults={
            'control_group': 'M',
            'format': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
            'versionable': True,
        })
    ''':class:`XmlDatastream` for the required Fedora **DC** datastream;
    datastream content will be automatically loaded as an instance of
    :class:`eulxml.xmlmap.dc.DublinCore`. This has been overridden to be a managed and versionable datastream.'''

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
            # reverse() encodes the PID_TOKEN and the :, so just unquote the url
            # (shouldn't contain anything else that needs escaping)
            target = urllib.unquote(target)

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

    @property
    def content_md5(self):
        '''In order to support duplicate checking before ingest,
        DigitalObject subclasses should implement this to return the MD5 checksum
        for the primary content datastream of that object, or None for non-content
        objects such as collections.'''
        raise NotImplementedError('Extending classes should implement content_md5')

    def index_data(self):
        data = super(DigitalObject, self).index_data()

        # index content checksum if available
        # (possibly redundant, but ensure it gets indexed if we have one)
        if self.content_md5 is not None:
            data['content_md5'] = self.content_md5

        if self.ingest_user:
            data['ingest_user'] = self.ingest_user
            data['added_by'] = user_full_name(self.ingest_user)
        data['audit_trail_users'] = list(self.audit_trail_users)
        data['users'] = [user_full_name(u) for u in self.audit_trail_users]

        # used to group migrated objects; set on all objects so everything
        # can be grouped and sorted in the same way
        data['original_pid'] = self.pid
        return data

    def save(self, logMessage=None):
        # check for duplicate content before initial ingest
        if self._create and self.content_md5 is not None:
            solr = solr_interface()
            q = solr.query(content_md5=self.content_md5).field_limit(['pid', 'content_model'])
            # if a duplicate is found, raise custom exception with info on the dupes
            if q.count():
                msg = 'Detected %s duplicate record%s' % \
                    (q.count(), 's' if q.count() != 1 else '')

                results = list(q)
                pids = [r['pid'] for r in results]
                # dictionary of pid : list of cmodels
                pid_cmodels = dict([(r['pid'], r['content_model']) for r in results])

                raise DuplicateContent(msg, pids, pid_cmodels)

        return super(DigitalObject, self).save(logMessage)


    # map datastream IDs to human-readable names for inherited history_events method
    # (common datastream IDs only here)
    component_key = {
        'MODS': 'descriptive metadata',
        'DC': 'descriptive metadata',
        'Rights': 'rights metadata',
        'RELS-EXT': 'related objects',
    }

    def history_events(self):
        '''Cluster API calls documented in the
        :attr:`eulfedora.models.DigitalObject.audit_trail` into
        "events", i.e. when updating an object requires updating
        multiple datastreams and making multiple API calls.

        :returns: list of :class:`AuditTrailEvent`
        '''

        events = []
        if self.audit_trail:
            current = None
            for r in self.audit_trail.records:
                # if there is an event started, check if this record
                # belongs to it
                if current:
                    # To be part of the same "event", the username and message
                    # must match, and the datetime should be within 5 seconds
                    # of the last update.  If any of those are untrue,
                    # close the last event and start a new one.
                    if r.user != current.user or r.message != current.message \
                       or r.component in current.components \
                       or (r.date - current.date) > timedelta(seconds=6):
                        # add the event to the list - complete;
                        events.append(current)
                        current = None  # trigger to start a new event
                    else:
                        # add to the current event
                        current.add_record(r)

                if current is None:
                    # init a new event
                    current = AuditTrailEvent(r, self.component_key)

            # add the last event to the list
            events.append(current)

        return events


def user_full_name(username):
    # get full name if possible from username
    name = None
    try:
        u = get_user_model().objects.get(username=username)
        name = u.get_full_name()
    except ObjectDoesNotExist:
        pass

    if not name:
        name = username

    return name


class Repository(server.Repository):
    """Extend the Django-ized Fedora Repository object to take a request object
    and connect to Fedora using a user is logged in and the required credentials
    are available.  If no request is specified or no user is logged in, falls
    back to the default logic, which uses Django settings for Fedora credentials.
    """

    default_object_type = ArkPidDigitalObject

    def __init__(self, username=None, password=None, request=None):
        if request is not None and request.user.is_authenticated() and \
            'fedora_password' in request.session:
                username = request.user.username
                password = decrypt(request.session['fedora_password'])
        super(Repository, self).__init__(username=username, password=password)


class TypeInferringRepository(server.TypeInferringRepository, Repository):
    '''Make :class:`eulfedora.server.TypeInferringRepository`
    available with local defaults, based on :class:`Repository`
    subclass.
    '''
    pass

# TODO: think about better ways to make re-usable views that apply to
# objects across the project (also relevant to xml datastream and
# audit trail views)

def history_view(request, pid, type=ArkPidDigitalObject,
                 template_name='common/history.html'):
    '''Re-usable view for displaying a human-readable version of the
    history of a :class:`DigitalObject`.

    :param request: http request
    :param pid: object pid for which history should be displayed
    :param type: optional subclass of :class:`DigitalObject`; if the
	object does not have the appropriate content models, the view will
        404
    :param template_name: optional template to use when rendering this
	view
    '''

    repo = Repository(request=request)
    obj = repo.get_object(pid, type=type)
    try:
        # if this is not actually the right type of DigitalObject,
        # then 404 (object is not available at this url)
        if not obj.has_requisite_content_models:
            raise Http404
        return render(request, template_name, {'obj' : obj})

    except PermissionDenied:
        # Fedora may return a PermissionDenied error when accessing a datastream
        # where the datastream does not exist, object does not exist, or user
        # does not have permission to access the datastream

        # check that the object exists - if not, 404
        if not obj.exists:
            raise Http404
        # for now, assuming that if object exists and has correct content models,
        # it will have all the datastreams required for this view

        return HttpResponseForbidden('Permission Denied to access %s' % pid,
                                     content_type='text/plain')

    except RequestFailed as rf:
        # if fedora actually returned a 404, propagate it
        if rf.code == 404:
            raise Http404

        msg = 'There was an error contacting the digital repository. ' + \
              'This prevented us from accessing data. If this ' + \
              'problem persists, please alert the repository ' + \
              'administrator.'
        return HttpResponse(msg, content_type='text/plain', status=500)


# alias for now, clean up later
DigitalObject = ArkPidDigitalObject
