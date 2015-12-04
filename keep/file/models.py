import glob
import logging
import urllib

from keep.common.models import PremisFixity, PremisObject
import os
import magic
import bagit
from django.conf import settings
from django.db import models
from eulcm.xmlmap.boda import Rights
from eulfedora.models import FileDatastream, XmlDatastream, Relation, \
    FileDatastreamObject
from eulfedora.rdfns import relsext
from eulxml import xmlmap
from eulxml.xmlmap import mods, premis
from keep.common.fedora import DigitalObject, LocalMODS, Repository
from keep.common.rdfns import REPO
from keep.collection.models import CollectionObject
from keep.file.utils import md5sum, sha1sum


logger = logging.getLogger(__name__)

## DB model for creating application

class Application(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=30)

    def __unicode__(self):
        return '%s %s' % (self.name, self.version)


class Disk_Image(models.Model):
    'Place-holder DB model to define permissions for disk image objects'
    class Meta:
        permissions = (
            ("view_disk_image", "Can view, search, and browse disk images"),
            ("manage_disk_image_supplements", "Can manage disk image supplemental files"),
        )


##
## Fedora DiskImage
##

class DiskImageMods(LocalMODS):
    '''Customized MODS for :class:`DiskImage`, based on
    :class:`~keep.common.fedora.LocalMODS`.'''
    # FIXME: should really just be a date field and not datetime
    coveringdate_start = xmlmap.StringField('mods:originInfo/mods:dateCreated[@point="start"]')
    '''coverage start date (dateCreated start, as :class:`~eulxml.xmlmap.StringField`
    to allow any of YYYY, YYYY-MM, or YYYY-MM-DD date formats)'''
    coveringdate_end = xmlmap.StringField('mods:originInfo/mods:dateCreated[@point="end"]')
    'coverage end date (dateCreated start, as :class:`~eulxml.xmlmap.StringField`)'
    genre = xmlmap.StringField('mods:genre[@authority="aat"]')
    'convience mapping for genre, for easy display on disk image edit form'


class DiskImagePremis(premis.Premis):
    XSD_SCHEMA = premis.PREMIS_SCHEMA

    object = xmlmap.NodeField('p:object', PremisObject)

    fixity_checks = xmlmap.NodeListField('p:event[p:eventType="fixity check"]',
        premis.Event)
    '''list of PREMIS fixity check events (where event type is "fixity check"),
     as instances of :class:`eulxml.xmlmap.premis.Event`'''


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

    diskimage_mimetypes = [
        'application/x-aff',    # AFF, advanced forensic format
        'application/x-ad1',    # AD1, proprietary disk image format
        'application/x-iso9660-image', # ISO
        'application/x-ewf', # E01 Expert Witness Format
        'application/x-tar', # tar file
        'application/mbox'  # mbox (? may require extra magic file entries)
    ]

    # mapping of mimetype to format label to insert in Premis
    mimetype_format = {
        'application/x-aff': 'AFF',
        'application/x-ad1': 'AD1',
        'application/x-iso9660-image': 'ISO',
        'application/x-ewf': 'E01',
        'application/x-tar': 'TAR',
        'application/mbox': 'MBOX'
    }

    allowed_mimetypes = ['', 'application/octet-stream'] + diskimage_mimetypes
    # NOTE: empty type and application/octet-stream are required for javascript upload,
    # because browser does not detect any mimetype at all for AFF and AD1 files
    # and detects ISO as the generic application/octet-stream
    # NOTE: Mimetypes for AD1 and AFF are custom mimetypes and must be configured
    # in your local magic files.  See the deploy notes for more information.

    collection = Relation(relsext.isMemberOfCollection, type=CollectionObject)
    ''':class:`~keep.collection.models.CollectionObject that this object belongs to,
    via `isMemberOfCollection` relation.
    '''

    #: original DiskImage object that this DiskImage is related to, if
    #: this is a migrated object; related via fedora-rels-ext isDerivationOf
    original = Relation(relsext.isDerivationOf, type='self')
    #: migrated DiskImage object that supercedes this object, if a
    #: migration has occurred; related via fedora-rels-ext hasDerivation
    migrated = Relation(relsext.hasDerivation, type='self')

    mods = XmlDatastream("MODS", "MODS Metadata", DiskImageMods, defaults={
                         'control_group': 'M',
                         'format': mods.MODS_NAMESPACE,
                         'versionable': True,
                         })
    '''descriptive metadata as MODS - :class:`~eulfedora.models.XmlDatastream`
    with content as :class:`LocalMods`'''
    # note: using base local mods for now; may need to extend for disk images

    content = FileDatastream("content", "Master disk image file", defaults={
                             'versionable': False,
                             })
    'master disk image binary content as :class:`~eulfedora.models.FileDatastream`'
    # NOTE: could be one of a few allowed mimetypes

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
        'RELS-EXT': 'collection membership or last fixity check',  # TODO: revise as we add more relations
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

    @property
    def has_supplemental_content(self):
        '''Boolean to indicate if this disk image object has any supplemental
        file datastreams.

        .. Note:: only works on saved objects
        '''
        return any(dsid.startswith('supplement') for dsid in self.ds_list.keys())

    @property
    def supplemental_content(self):
        '''Generator for supplemental content datastreams'''
        for dsid in self.ds_list.keys():
            if dsid.startswith('supplement'):
                yield self.getDatastreamObject(dsid)

    _content_checksum = None
    '''Used as a workaround for Fedora 3.4 issue with file URIs and checksums
    and to support duplicate detection based on checksums, store
    content checksum without sending it to Fedora.'''

    @property
    def content_md5(self):
        return self._content_checksum or self.content.checksum


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
        if self.mods.content.coveringdate_start and \
           self.mods.content.coveringdate_end:
            # FIXME: not sure the best way to indicate date range here
            self.dc.content.coverage_list.append('%s:%s' %
                (self.mods.content.coveringdate_start, self.mods.content.coveringdate_end))

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
    def init_from_file(filename, initial_label=None, request=None, checksum=None,
        mimetype=None, content_location=None, sha1_checksum=None):
        '''Static method to create a new :class:`DiskImage` instance from
        a file.  Sets the object label and metadata title based on the initial
        label specified, or file basename.

        :param filename: full path to the disk image file, as a string
        :param initial_label: optional initial label to use; if not specified,
            the base name of the specified file will be used
        :param request: :class:`django.http.HttpRequest` passed into a view method;
            must be passed in order to connect to Fedora as the currently-logged
            in user
        :param checksum: the MD5 checksum of the file being sent to fedora.
        :param mimetype: the mimetype for the main disk image content.
        :param content_location: optional file URI for file-based Fedora ingest
        :param sha1_checksum: the SHA1 checksum of the file being sent to fedora,
            for storage in the PREMIS technical metadata. Note that SHA-1 will
            be calculated if not passed in (slow for large files).
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
               initial_label.lower().endswith('.ad1') or \
               initial_label.lower().endswith('.iso'):
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

        # Set the file checksum
        obj.content.checksum = checksum
        # set mimetype
        if mimetype is None:
            # if no mimetype was passed in, determine from file
            m = magic.Magic(mime=True)
            mtype = m.from_file(filename)
            mimetype, separator, options = mtype.partition(';')
        obj.content.mimetype = mimetype

        # Set disk image datastream label to filename
        obj.content.label = initial_label

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
        # add sha-1 to checksums in premis; calculate if not passed in
        if sha1_checksum is None:
            sha1_checksum = sha1sum(filename)
        obj.provenance.content.object.checksums.append(PremisFixity(algorithm='SHA-1'))
        obj.provenance.content.object.checksums[1].digest = sha1_checksum

        obj.provenance.content.object.create_format()
        # set format based on mimetype
        if mimetype in DiskImage.mimetype_format:
            obj_format = DiskImage.mimetype_format[mimetype]
        else:
            # as a fallback, use the file extension for format
            obj_format = ext.upper().strip('.')
        obj.provenance.content.object.format.name = obj_format

        # if a content URI is specified (e.g. for large files), use that
        if content_location is not None:
            obj.content.ds_location = content_location
        # otherwise set the file as content to be posted
        else:
            obj.content.content = open(filename)
            # FIXME: at what point does/should this file get closed?

        # descriptive/technical metadata todo

        return obj

    @staticmethod
    def init_from_bagit(path, request=None, file_uri=True):
        '''Static method to create a new :class:`DiskImage` instance from
        a BagIt.  Sets the object label and metadata title based on the
        name of the bag, and looks for a supported disk image file type
        (e.g. AFF or AD1) to use as the content datastream for the object.
        Content checksum is pulled from the BagIt metadata, and repository
        ingest will be done via file URIs based on configured
        **LARGE_FILE_STAGING_DIR** and **LARGE_FILE_STAGING_FEDORA_DIR**
        to better support ingesting large files (unless file_uri
        is False).

        Raises an exception if BagIt is not valid or if it does not
        contain a supported disk image data file.  (Note: using fast validation
        without checksum calculation, to minimize the time required to ingest
        large files.)

        :param path: full path to the BagIt directory that contains
            a disk image file
        :param request: :class:`django.http.HttpRequest` passed into a view method;
            must be passed in order to connect to Fedora as the currently-logged
            in user
        :param file_uri: ingest BagIt data via file uris based on
            configured staging directories (default behavior)
            instead of uploading the content to Fedora

        :returns: :class:`DiskImage` initialized from the BagIt contents
        '''

        # TODO: add optional file uri ingest flag, default to false
        # (mostly to allow testing)
        # - for all data files other than disk image, add
        # supplementN datastream with mimetype/filename as label/checksum
        # see if eulfedora getDatastreamObject can be used to init
        # a new/unmapped ds?

        bag = bagit.Bag(path)
        # NOTE: using fast validation here to avoid recalculating checksums
        # for very large files; only checksum compare will be done by fedora
        bag.validate(fast=True)  # raises bagit.BagValidationError if not valid

        # use the base name of the BagIt as initial object label
        initial_label = os.path.basename(path)

        # identify disk image content file within the bag
        content_file = None
        m = magic.Magic(mime=True)
        supplemental_files = []
        supplement_mimetypes = {}
        diskimage_mimetype = None
        # loop through bag content until we find a supported disk image file
        for data_path in bag.payload_files():
            # path is relative to bag root dir
            filename = os.path.join(path, data_path)
            mtype = m.from_file(filename)
            mimetype, separator, options = mtype.partition(';')
            if mimetype in DiskImage.diskimage_mimetypes:
                checksum_err_msg = '%%s checksum not found for disk image %s' \
                    % os.path.basename(data_path)
                # require both MD5 and SHA-1 for disk image to ingest
                try:
                    md5_checksum = bag.entries[data_path]['md5']
                except KeyError:
                    raise Exception(checksum_err_msg % 'MD5')
                try:
                    sha1_checksum = bag.entries[data_path]['sha1']
                except KeyError:
                    raise Exception(checksum_err_msg % 'SHA-1')

                # this is the disk image content file
                # store file and mimetype for further initialization
                content_file = filename
                diskimage_mimetype = mimetype

            # any data file that is not a disk image should be assumed
            # to be a supplemental file
            else:
                supplemental_files.append(filename)
                # store the mimetype so we don't have to recalculate
                supplement_mimetypes[filename] = mimetype

        # no disk image data found
        if content_file is None:
            raise Exception('No disk image content found in %s' % os.path.basename(path))

        optional_args = {}
        if file_uri:
            ingest_location = 'file://%s' % urllib.quote(content_file)
            # if Fedora base path is different from locally mounted staging directory,
            # convert from local path to fedora server path
            if getattr(settings, 'LARGE_FILE_STAGING_FEDORA_DIR', None) is not None:
                ingest_location = ingest_location.replace(settings.LARGE_FILE_STAGING_DIR,
                    settings.LARGE_FILE_STAGING_FEDORA_DIR)

            optional_args['content_location'] = ingest_location

        img = DiskImage.init_from_file(content_file, initial_label=initial_label,
            checksum=md5_checksum, mimetype=diskimage_mimetype, request=request,
            sha1_checksum=sha1_checksum, **optional_args)

        i = 0
        for i in range(len(supplemental_files)):
            sfile = supplemental_files[i]
            dsid = 'supplement%d' % i
            dsobj = img.getDatastreamObject(dsid, dsobj_type=FileDatastreamObject)
            dsobj.label = os.path.basename(sfile)
            dsobj.mimetype = supplement_mimetypes[sfile]
            # convert to relative path *within* the bag for BagIt metadata lookup
            data_path = sfile.replace(path, '').lstrip('/')
            dsobj.checksum = bag.entries[data_path]['md5']
            logger.debug('Adding supplemental dastream %s label=%s mimetype=%s checksum=%s' % \
                (dsid, dsobj.label, dsobj.mimetype, dsobj.checksum))


            if file_uri:
                ingest_location = 'file://%s' % urllib.quote(sfile)
                # if Fedora base path is different from locally mounted staging directory,
                # convert from local path to fedora server path
                if getattr(settings, 'LARGE_FILE_STAGING_FEDORA_DIR', None) is not None:
                    ingest_location = ingest_location.replace(settings.LARGE_FILE_STAGING_DIR,
                        settings.LARGE_FILE_STAGING_FEDORA_DIR)

                dsobj.ds_location = ingest_location
            else:
                # will probably only work for small/test content
                dsobj.content = open(sfile).read()

        return img

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
        # FIXME: is born-digital type still needed for anything? perms?
        # data['object_type'] = 'born-digital'
        data['object_type'] = 'disk image'
        # set as born digital for now; eventually, we'll need to distinguish
        # between kinds of born digital content

        if self.collection and self.collection.exists:

            # collection_source_id  (0 is an allowable id, so check not None)
            if self.collection.mods.content.source_id is not None:
                data['collection_source_id'] = self.collection.mods.content.source_id

            data['collection_id'] = self.collection.pid
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

        if self.provenance.content.fixity_checks:
            last_fixity_check = self.provenance.content.fixity_checks[-1]
            data['last_fixity_check'] = last_fixity_check.date
            data['last_fixity_result'] = last_fixity_check.outcome

        # store disk image format and size
        # - some disk images (i.e., objects migrated from AD1/AFF)
        # will have two sets of object characteristics; we want the
        # format from the last one listed
        if self.provenance.content.object and \
          self.provenance.content.object.latest_format:
            data['content_format'] = self.provenance.content.object.latest_format.name

        data['content_size'] = self.content.size

        if self.original:
            data['original_pid'] = self.original.pid

        return data


def large_file_uploads():
    '''Generate a list of BagIt uploaded to the configured large-file
    staging space and available for ingest.  Returns a list of directory
    names.'''
    upload_dir = getattr(settings, 'LARGE_FILE_STAGING_DIR')
    if upload_dir and os.path.isdir(upload_dir):
        # large file upload currently only supports BagIt SIPs, so ignore anythng else
        dbags = glob.glob('%s/diskimage/*/bagit.txt' % upload_dir.rstrip('/'))
        vbags = glob.glob('%s/video/*/bagit.txt' % upload_dir.rstrip('/'))
        bags = dbags + vbags
        return [os.path.dirname(b) for b in bags]
    else:
        logger.warning('LARGE_FILE_STAGING_DIR does not seem to be configured correctly')
        return []

