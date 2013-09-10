import os

from django.db import models
from eulcm.xmlmap.boda import Rights
from eulfedora.models import FileDatastream, XmlDatastream, Relation
from eulfedora.rdfns import relsext
from eulxml import xmlmap
from eulxml.xmlmap import mods, premis

from keep.common.fedora import DigitalObject, LocalMODS, Repository
from keep.collection.models import CollectionObject
from keep.file.utils import md5sum, sha1sum


## DB model for creating application

class Application(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=30)

    def __unicode__(self):
        return '%s %s' % (self.name, self.version)


##
## Fedora DiskImage
##

class DiskImageMods(LocalMODS):
    '''Customized MODS for :class:`DiskImage`, based on
    :class:`~keep.common.fedora.LocalMODS`.'''
    # FIXME: should really just be a date field and not datetime
    dateissued_start = xmlmap.DateField('mods:originInfo/mods:dateIssued[@point="start"]',
                                        format="%Y-%m-%d")
    'coverage start date (dateIssued start, as :class:`~eulxml.xmlmap.DateField`)'
    dateissued_end = xmlmap.DateField('mods:originInfo/mods:dateIssued[@point="end"]',
                                      format="%Y-%m-%d")
    'coverage end date (dateIssued start, as :class:`~eulxml.xmlmap.DateField`)'


class PremisFixity(premis.BasePremis):
    ROOT_NAME = 'fixity'
    algorithm = xmlmap.StringField('p:messageDigestAlgorithm')
    digest = xmlmap.StringField('p:messageDigest')

class PremisObjectFormat(premis.BasePremis):
    ROOT_NAME = 'format'
    name = xmlmap.StringField('p:formatDesignation/p:formatName')
    version = xmlmap.StringField('p:formatDesignation/p:formatVersion')

class PremisCreatingApplication(premis.BasePremis):
    ROOT_NAME = 'creatingApplication'
    name = xmlmap.StringField('p:creatingApplicationName')
    version = xmlmap.StringField('p:creatingApplicationVersion')
    date = xmlmap.DateField('p:dateCreatedByApplication')

class PremisObject(premis.Object):
    composition_level = xmlmap.IntegerField('p:objectCharacteristics/p:compositionLevel')
    checksums = xmlmap.NodeListField('p:objectCharacteristics/p:fixity',
                                     PremisFixity)
    format = xmlmap.NodeField('p:objectCharacteristics/p:format',
                              PremisObjectFormat)
    creating_application = xmlmap.NodeField('p:objectCharacteristics/p:creatingApplication',
                                            PremisCreatingApplication)

class DiskImagePremis(premis.Premis):

    object = xmlmap.NodeField('p:object', PremisObject)


class DiskImage(DigitalObject):
    '''Fedora object for Disk Images.  Extends :class:`~keep.common.fedora.DigitalObject`.
    '''

    # NOTE about datastream naming conventions
    # Where a corresponding datastream id already exists within the Keep
    # (i.e. MODS for mods metadata), the same datastream id will be used
    # Where a Keep datastream id does not already exist (e.g., Premis), following
    # Hydra content model conventions, based on generic simple Hydra content model
    # For documentation on Hydra content models, see:
    #   https://wiki.duraspace.org/display/hydra/Hydra+objects%2C+content+models+%28cModels%29+and+disseminators
    #   https://wiki.duraspace.org/display/hydra/Hydra+objects%2C+content+models+%28cModels%29+and+disseminators#Hydraobjects%2Ccontentmodels%28cModels%29anddisseminators-genericContent

    DISKIMAGE_CONTENT_MODEL = 'info:fedora/emory-control:DiskImage-1.0'
    CONTENT_MODELS = [DISKIMAGE_CONTENT_MODEL]
    NEW_OBJECT_VIEW = 'file:view'

    allowed_mimetypes = ['', 'application/x-aff', 'application/x-ad1']
    # NOTE: '' is required for javascript, because browser does not detect
    # any mimetype at all for AFF and AD1 files
    # NOTE: These are custom mimetypes and must be configured in your local
    # magic files.  See the deploy notes for more information.

    collection = Relation(relsext.isMemberOfCollection, type=CollectionObject)
    ''':class:`~keep.collection.models.CollectionObject that this object belongs to,
    via `isMemberOfCollection` relation.
    '''

    mods = XmlDatastream("MODS", "MODS Metadata", DiskImageMods, defaults={
                         'control_group': 'M',
                         'format': mods.MODS_NAMESPACE,
                         'versionable': True,
                         })
    '''descriptive metadata as MODS - :class:`~eulfedora.models.XmlDatastream`
    with content as :class:`LocalMods`'''
    # note: using base local mods for now; may need to extend for disk images

    content = FileDatastream("content", "Master disk image file", defaults={
                             #'mimetype': 'audio/x-wav',
                             'versionable': True,  # ? (maybe)
                             })
    'master disk image binary content as :class:`~eulfedora.models.FileDatastream`'
    # TODO: coudl be one of several allowed mimetypes

    rights = XmlDatastream("Rights", "Usage rights and access control metadata", Rights,
                           defaults={
                               'control_group': 'M',
                               'versionable': True,
                           })
    '''access control metadata :class:`~eulfedora.models.XmlDatastream`
    with content as :class:`Rights`'''

    provenance = XmlDatastream('provenanceMetadata',
                               'Provenance metadata', DiskImagePremis, defaults={
                               'versionable': False
                               })
    '''``provenanceMetadata`` datastream for PREMIS object metadata; datastream
    XML content will be an instance of :class:`eulxml.xmlmap.premis.Premis`.'''

    # map datastream IDs to human-readable names for inherited history_events method
    component_key = {
        'MODS': 'descriptive metadata',
        'DC': 'descriptive metadata',
        'Rights': 'rights metadata',
        'RELS-EXT': 'collection membership',  # TODO: revise when/if we add more relations
        'provenanceMetadata': 'provenance metadata',
    }

    def get_default_pid(self):
        # extend common default pid logic in to also set ARK identifier
        # in the premis object
        pid = super(DiskImage, self).get_default_pid()

        if self.mods.content.ark:
            self.provenance.content.object.id = self.mods.content.ark
            self.provenance.content.object.id_type = 'ark'

        return pid


    # NOTE: auto-calculated information such as checksums stored in premis
    # will need to be updated anytime the master disk image datastream is updated
    # (will probably need to extend the save method for this)

    def save(self, logMessage=None):
        '''Save the object.  If the content of any :class:`~AudioObject.mods`,
        :class:`AudioObject.rels_ext`, or :class:`AudioObject.digitaltech`
        datastreams have been changed, the DC will be updated and saved as well.

        :param logMessage: optional log message
        '''
        if not self.exists or self.mods.isModified() or \
            self.rels_ext.isModified() or self.rights.isModified():
            # DC is derivative metadata.
            # If this is a new item (does not yet exist in Fedora)
            # OR if any of the relevant datastreams have changed, update it.
            self._update_dc()

        return super(DiskImage, self).save(logMessage)

    def _update_dc(self):
        '''Update Dublin Core (derivative metadata) based on master metadata
        from MODS, RELS-EXT, and rights metadata in order to keep data
        synchronized and make fields that need to be searchable accessible to
        Fedora findObjects API method.
         '''
        # NOTE: borrowed almost completely from audio, with minor modifications
        # TODO: move to common code somewhere?

        # identifiers
        del(self.dc.content.identifier_list)        # clear out any existing names

        # title
        if self.mods.content.title:
            # not strictly DC, but also keep object label in sync with MODS title
            self.label = self.mods.content.title
            self.dc.content.title = self.mods.content.title
        if self.mods.content.resource_type:
            self.dc.content.type = self.mods.content.resource_type

        # clear out any dates previously in DC
        del(self.dc.content.coverage_list)
        if self.mods.content.dateissued_start and \
           self.mods.content.dateissued_end:
            # FIXME: not sure the best way to indicate date range here
            self.dc.content.coverage_list.append('%s:%s' %
                (self.mods.content.dateissued_start, self.mods.content.dateissued_end))

        # clear out any descriptions previously in DC and set from MODS abstract
        del(self.dc.content.description_list)
        if self.mods.content.abstract and \
           self.mods.content.abstract.text:
            self.dc.content.description_list.append(self.mods.content.abstract.text)

        # clear out any rights previously in DC and set contents from Rights accessStatus
        del(self.dc.content.rights_list)
        if self.rights.content.access_status:
            # set dc:rights to text of access status
            self.dc.content.rights_list.append(self.rights.content.access_status.text)


    @staticmethod
    def init_from_file(filename, initial_label=None, request=None, checksum=None):
        '''Static method to create a new :class:`DiskImage` instance from
        a file.  Sets the object label and metadata title based on the initial
        label specified, or file basename.

        :param filename: full path to the disk image file, as a string
        :param initial_label: optional initial label to use; if not specified,
            the base name of the specified file will be used
        :param request: :class:`django.http.HttpRequest` passed into a view method;
            must be passed in order to connect to Fedora as the currently-logged
            in user
        :param checksum: the checksum of the file being sent to fedora.
        :returns: :class:`DiskImage` initialized from the file
        '''

        # if no checksum was passed in, calculate one
        if checksum is None:
            checksum = md5sum(filename)

        basename, ext = os.path.splitext(os.path.basename(filename))

        # ajax upload passes original filename as initial label
        if initial_label is not None:
            # if initial label looks like a file, strip off the extension
            # for the object name/title
            if initial_label.lower().endswith('.aff') or \
               initial_label.lower().endswith('.ad1'):
                basename, ext = os.path.splitext(initial_label)
                # NOTE: also using extension from original filename
                # here because in some cases (under apache?) uploaded file
                # names do not have the original extension
                initial_label = basename

        else:
            initial_label = basename

        repo = Repository(request=request)
        obj = repo.get_object(type=DiskImage)
        # set initial object label from the base filename
        obj.label = initial_label
        obj.mods.content.title = obj.label
        obj.dc.content.title = obj.label
        # set initial mods:typeOfResource - same for all Disk Images
        obj.mods.content.resource_type = 'software, multimedia'
        # set genre as born digital
        obj.mods.content.genres.append(mods.Genre(authority='aat', text='born digital'))

        # premis data
        obj.provenance.content.create_object()
        # NOTE: premis object id will be same as short-form ARK stored in MODS
        # It cannot be set until pid is minted, which will happen in get_default_pid,
        # but premis is order dependent so add a place-holder here
        obj.provenance.content.object.id_type = 'ark'
        obj.provenance.content.object.id = ''

        # object type required to be schema valid, must be in premis namespace
        obj.provenance.content.object.type = 'p:file'

        # composition level required for object characteristics; probably should be 0 (?)
        obj.provenance.content.object.composition_level = 0
        # store checksums in premis: MD5 (already calculated) and SHA-1
        # picky about order here too: force algorithm to be added first
        obj.provenance.content.object.checksums.append(PremisFixity(algorithm='MD5'))
        obj.provenance.content.object.checksums[0].digest = checksum
        obj.provenance.content.object.checksums.append(PremisFixity(algorithm='SHA-1'))
        obj.provenance.content.object.checksums[1].digest = sha1sum(filename)

        obj.provenance.content.object.create_format()
        # for now, format name will be upper-cased version of file extension
        # (i.e., AFF or AD1)
        obj.provenance.content.object.format.name = ext.upper().strip('.')


        obj.content.content = open(filename)  # FIXME: at what point does/should this get closed?
        # Set the file checksum
        obj.content.checksum = checksum
        # Set disk image datastream label to filename
        obj.content.label = initial_label

        # descriptive/technical metadata todo

        return obj

    @models.permalink
    def get_absolute_url(self):
        'Absolute url to view this object within the site'
        return (DiskImage.NEW_OBJECT_VIEW, [str(self.pid)])

    def index_data(self):
        '''Extend the default
        :meth:`eulfedora.models.DigitalObject.index_data`
        method to include additional fields specific to Keep and for
        disk images.'''
        # NOTE: we don't want to rely on other objects being indexed in Solr,
        # so index data should not use Solr to find any related object info

        data = super(DiskImage, self).index_data()
        data['object_type'] = 'born-digital'
        # set as born digital for now; eventually, we'll need to distinguish
        # between kinds of born digital content

        if self.collection and self.collection.exists:

            # collection_source_id  (0 is an allowable id, so check not None)
            if self.collection.mods.content.source_id is not None:
                data['collection_source_id'] = self.collection.mods.content.source_id

            data['collection_id'] = self.collection.uri
            data['collection_label'] = self.collection.label

        # include resolvable ARK if available
        if self.mods.content.ark_uri:
            data['ark_uri'] = self.mods.content.ark_uri

        if self.content.checksum:
            data['content_md5'] = self.content.checksum

        # copied from audio; enable once we have rights editing
        # # rights access status code
        # if self.rights.content.access_status:
        #     data['access_code'] = self.rights.content.access_status.code
        # # copyright date from rights metadata
        # if self.rights.content.copyright_date:
        #     data['copyright_date'] = self.rights.content.copyright_date
        # # ip note from rights metadata
        # if self.rights.content.ip_note:
        #     data['ip_note'] = self.rights.content.ip_note


        return data



