from django.db import models
from keep.common.fedora import DigitalObject
from eulfedora.models import FileDatastream, XmlDatastream, Relation
from eulfedora.rdfns import relsext
from keep.collection.models import CollectionObject
from keep.common.fedora import DigitalObject, Repository, LocalMODS
from eulxml import xmlmap
from eulxml.xmlmap import mods
from eulxml.xmlmap import premis
import os
from keep.common.models import _BaseDigitalTech
from pymediainfo import MediaInfo
import bagit
import magic
from django.conf import settings
import urllib
from keep.file.utils import md5sum, sha1sum
from keep.common.models import PremisFixity, PremisObject

import logging


logger = logging.getLogger(__name__)



class VideoMods(LocalMODS):
    '''Customized MODS for :class:`Video`, based on
    :class:`~keep.common.fedora.LocalMODS`.'''
    # general_note = xmlmap.NodeField('mods:note[@type="general"]',
    #       mods.TypedNote, required=False)
    # ':class:`~eulxml.xmlmap.mods.TypedNote` with `type="general"`'
    # part_note = xmlmap.NodeField('mods:note[@type="part number"]',
    #                              mods.TypedNote)
    # ':class:`~eulxml.xmlmap.mods.TypedNote` with `type="part number"`'
    #
    # dm1_id = xmlmap.StringField('mods:identifier[@type="dm1_id"]',
    #         required=False, verbose_name='Record ID/Filename')
    # dm1_other_id = xmlmap.StringField('mods:identifier[@type="dm1_other"]',
    #         required=False, verbose_name='Other ID')


class VideoPremis(premis.Premis):
    XSD_SCHEMA = premis.PREMIS_SCHEMA

    object = xmlmap.NodeField('p:object', PremisObject)

    fixity_checks = xmlmap.NodeListField('p:event[p:eventType="fixity check"]',
        premis.Event)
    '''list of PREMIS fixity check events (where event type is "fixity check"),
     as instances of :class:`eulxml.xmlmap.premis.Event`'''




class DigitalTech(_BaseDigitalTech):
    ":class:`~eulxml.xmlmap.XmlObject` for Digital Technical Metadata."
    ROOT_NAME = 'digitaltech'
    # date_captured = xmlmap.StringField('dt:dateCaptured[@encoding="w3cdtf"]',
    #     help_text='Date digital capture was made', required=True)
    # 'date digital capture was made (string)'
    codec_quality = xmlmap.StringField('dt:codecQuality', required=True,
        help_text='Whether the data compression method was lossless or lossy')
    'codec quality - lossless or lossy'
    duration = xmlmap.IntegerField('dt:duration/dt:measure[@type="time"][@unit="seconds"][@aspect="duration of playing time"]',
        help_text='Duration of video playing time', required=True)
    'duration of the vidoe file'


class Video(DigitalObject):
    '''Fedora Video Object.  Extends :class:`~eulfedora.models.DigitalObject`.'''
    VIDEO_CONTENT_MODEL = 'info:fedora/emory-control:Video-1.0'
    CONTENT_MODELS = [VIDEO_CONTENT_MODEL]
    NEW_OBJECT_VIEW = 'video:view'

    # There are several mimetypes for MPEG files
    allowed_master_mimetypes = [
        'video/quicktime',
        'video/x-dv',
        'video/mpeg',
        'video/x-m4v',
        'video/x-msvideo'
    ]
    allowed_access_mimetypes = ['video/mp4']

    mods = XmlDatastream("MODS", "MODS Metadata", VideoMods, defaults={
            'control_group': 'M',
            'format': mods.MODS_NAMESPACE,
            'versionable': True,
        })

    digitaltech = XmlDatastream("DigitalTech", "Technical Metadata - Digital", DigitalTech,
        defaults={
            'control_group': 'M',
            'versionable': True,
        })
    '''digital technical metadata :class:`~eulfedora.models.XmlDatastream`
    with content as :class:`DigitalTech`'''


    'MODS :class:`~eulfedora.models.XmlDatastream` with content as :class:`VideoMods`'

    content = FileDatastream("VIDEO", "Video datastream", defaults={
            'versionable': True,
        })
    'master video :class:`~eulfedora.models.FileDatastream`'

    provenance = XmlDatastream('provenanceMetadata',
                               'Provenance metadata', VideoPremis, defaults={
                               'versionable': False
                               })
    '''``provenanceMetadata`` datastream for PREMIS object metadata; datastream
    XML content will be an instance of :class:`eulxml.xmlmap.premis.Premis`.'''

    access_copy = FileDatastream("CompressedVideo", "Compressed video datastream", defaults={
            'mimetype': 'video/mp4',
            'versionable': True,
        })
    'access copy of video :class:`~eulfedora.models.FileDatastream`'
    #
    #
    # sourcetech = XmlDatastream("SourceTech", "Technical Metadata - Source", SourceTech,
    #     defaults={
    #         'control_group': 'M',
    #         'versionable': True,
    #     })
    # '''source technical metadata :class:`~eulfedora.models.XmlDatastream` with content as
    # :class:`SourceTech`'''
    #
    # rights = XmlDatastream("Rights", "Usage rights and access control metadata", Rights,
    #     defaults={
    #         'control_group': 'M',
    #         'versionable': True,
    #     })
    # '''access control metadata :class:`~eulfedora.models.XmlDatastream`
    # with content as :class:`Rights`'''
    #
    # jhove = FileDatastream("JHOVE", "JHOVE datastream", defaults={
    #         'mimetype': 'application/xml',
    #         'control_group': 'M',
    #         'versionable': True,
    #         'format': 'http://hul.harvard.edu/ois/xml/xsd/jhove/jhove.xsd',
    #     })
    # 'JHOVE technical metadata for the master audio :class:`~eulfedora.models.FileDatastream`'
    # # JHOVE is xml, but treat it as a file for now since we're just storing it,
    # # not doing any processing, updating, etc.
    #
    # # map datastream IDs to human-readable names for inherited history_events method
    # component_key = {
    #     'AUDIO': 'audio (master)',
    #     'CompressedAudio': 'audio (access version)',
    #     'SourceTech': 'source technical metadata',
    #     'DigitalTech': 'digital technical metadata',
    #     'JHOVE': 'technical metadata',
    #     'MODS': 'descriptive metadata',
    #     'DC': 'descriptive metadata',
    #     'Rights': 'rights metadata',
    #     'RELS-EXT': 'collection membership',  # TODO: revise when/if we add more relations
    # }
    #
    collection = Relation(relsext.isMemberOfCollection, type=CollectionObject)
    ''':class:`~keep.collection.models.CollectionObject that this object is a member of,
    via `isMemberOfCollection` relation.
    '''
    _content_checksum = None
    '''Used as a workaround for Fedora 3.4 issue with file URIs and checksums
    and to support duplicate detection based on checksums, store
    content checksum without sending it to Fedora.'''

    @property
    def content_md5(self):
        return self._content_checksum or self.content.checksum

    def get_default_pid(self):
        # extend common default pid logic in to also set ARK identifier
        # in the premis object
        pid = super(Video, self).get_default_pid()

        if self.mods.content.ark:
            self.provenance.content.object.id = self.mods.content.ark
            self.provenance.content.object.id_type = 'ark'

        return pid


    #
    # def save(self, logMessage=None):
    #     '''Save the object.  If the content of any :class:`~AudioObject.mods`,
    #     :class:`AudioObject.rels_ext`, or :class:`AudioObject.digitaltech`
    #     datastreams have been changed, the DC will be updated and saved as well.
    #
    #     :param logMessage: optional log message
    #     '''
    #     if not self.exists or self.mods.isModified() or self.rels_ext.isModified() or \
    #         self.digitaltech.isModified() or self.rights.isModified():
    #         # DC is derivative metadata based on MODS/RELS-EXT/Digital Tech
    #         # If this is a new item (does not yet exist in Fedora)
    #         # OR if any of the relevant datastreams have changed, update DC
    #         self._update_dc()
    #
    #     # for now, keep object label in sync with MODS title
    #     if self.mods.isModified() and self.mods.content.title:
    #         self.label = self.mods.content.title
    #
    #     return super(AudioObject, self).save(logMessage)
    #
    @models.permalink
    def get_absolute_url(self):
        'Absolute url to view this object within the site'
        return ('video:view', [str(self.pid)])
    #
    # def get_access_url(self):
    #     "Absolute url to hear this object's access version"
    #     if self.compressed_audio.exists:
    #         return reverse('audio:download-compressed-audio',
    #                        args=[str(self.pid), self.access_file_extension()])
    #     # as of file migration (1.2), legacy DM access path is no longer needed
    #
    # def access_file_extension(self):
    #     '''Return the expected file extension for whatever type of
    #     compressed audio datastream the current object has (if it has
    #     one), based on the datastream mimetype.  Currently, compressed
    #     audio could be MP3 or M4A/MP4.'''
    #     if self.compressed_audio.exists:
    #         if self.compressed_audio.mimetype == 'audio/mpeg':
    #             return 'mp3'
    #         if self.compressed_audio.mimetype == 'audio/mp4':
    #             return 'm4a'
    #
    # @property
    # def conversion_result(self):
    #     '''Return the :class:`~eullocal.django.taskresult.models.TaskResult`
    #     for the most recently requested access copy conversion (if any).
    #     '''
    #     conversions = TaskResult.objects.filter(object_id=self.pid).order_by('-created')
    #     if conversions:
    #         return conversions[0]
    #
    # @property
    # def researcher_access(self):
    #     return allow_researcher_access(self.rights.content)
    #
    # def _update_dc(self):
    #     '''Update Dublin Core (derivative metadata) based on master metadata
    #     from MODS, RELS-EXT, and digital tech metadata in order to keep data
    #     synchronized and make fields that need to be searchable accessible to
    #     Fedora findObjects API method.
    #      '''
    #     # identifiers
    #     del(self.dc.content.identifier_list)        # clear out any existing names
    #
    #     # title
    #     if self.mods.content.title:
    #         self.label = self.mods.content.title
    #         self.dc.content.title = self.mods.content.title
    #     if self.mods.content.resource_type:
    #         self.dc.content.type = self.mods.content.resource_type
    #
    #     # creator names
    #     del(self.dc.content.creator_list)        # clear out any existing names
    #     for name in self.mods.content.names:
    #         # for now, use unicode conversion as defined in mods.Name
    #         self.dc.content.creator_list.append(unicode(name))
    #
    #     # clear out any dates previously in DC
    #     del(self.dc.content.date_list)
    #     if self.mods.content.origin_info and \
    #        len(self.mods.content.origin_info.created) and \
    #        self.mods.content.origin_info.created[0].date:
    #         self.dc.content.date_list.append(self.mods.content.origin_info.created[0].date)
    #     if self.mods.content.origin_info and \
    #        len(self.mods.content.origin_info.issued) and \
    #        self.mods.content.origin_info.issued[0].date:
    #         self.dc.content.date_list.append(self.mods.content.origin_info.issued[0].date)
    #
    #     # clear out any descriptions previously in DC and set from MODS/digitaltech
    #     del(self.dc.content.description_list)
    #     if self.mods.content.general_note and \
    #        self.mods.content.general_note.text:
    #         self.dc.content.description_list.append(self.mods.content.general_note.text)
    #
    #     # clear out any rights previously in DC and set contents from Rights accessStatus
    #     del(self.dc.content.rights_list)
    #     if self.rights.content.access_status:
    #         # access code no longer needs to be included, since we will not be searching
    #         self.dc.content.rights_list.append(self.rights.content.access_status.text)
    #
    # def index_data(self):
    #     '''Extend the default
    #     :meth:`eulfedora.models.DigitalObject.index_data`
    #     method to include additional fields specific to Keep
    #     Audio objects.'''
    #     # NOTE: we don't want to rely on other objects being indexed in Solr,
    #     # so index data should not use Solr to find any related object info
    #
    #     # FIXME: is it worth splitting out descriptive index data here?
    #     data = super(AudioObject, self).index_data()
    #     data['object_type'] = 'audio'
    #     if self.collection and self.collection.exists:
    #
    #         # collection_source_id  (0 is an allowable id, so check not None)
    #         if self.collection.mods.content.source_id is not None:
    #             data['collection_source_id'] = self.collection.mods.content.source_id
    #
    #         # FIXME: previously indexing URI; is this needed for any reason or can we
    #         # use pid?  (needs to match collection index pid field for solr join)
    #         # data['collection_id'] = self.collection.uri
    #         data['collection_id'] = self.collection.pid
    #         try:
    #             # pull parent & archive collection objects directly from fedora
    #             parent = CollectionObject(self.api, self.collection.uri)
    #             data['collection_label'] = parent.label
    #             # NB: as of 2011-08-23, eulindexer doesn't support automatic
    #             # reindexing of audio objects when their collection changes.
    #             # as a result, archive_id and archive_label may be stale.
    #             # disable indexing them until eulindexer supports those
    #             # chained updates.
    #             #data['archive_id'] = parent.collection_id
    #             #archive = CollectionObject(self.api, parent.collection_id)
    #             #data['archive_label'] = archive.label
    #         except RequestFailed as rf:
    #             logger.error('Error accessing collection or archive object in Fedora: %s' % rf)
    #
    #     # include resolvable ARK if available
    #     if self.mods.content.ark_uri:
    #         data['ark_uri'] = self.mods.content.ark_uri
    #
    #     # old identifiers from previous digital masters
    #     dm1_ids = []
    #     if self.mods.content.dm1_id:
    #         dm1_ids.append(self.mods.content.dm1_id)
    #     if self.mods.content.dm1_other_id:
    #         dm1_ids.append(self.mods.content.dm1_other_id)
    #     if dm1_ids:
    #         data['dm1_id'] = dm1_ids
    #
    #     # digitization purpose, if not empty
    #     if self.digitaltech.content.digitization_purpose_list:
    #         # convert nodelist to a normal list that can be serialized as json
    #         data['digitization_purpose'] = [dp for dp in self.digitaltech.content.digitization_purpose_list]
    #
    #     # related files
    #     if self.sourcetech.content.related_files_list:
    #         data['related_files'] = [rel for rel in self.sourcetech.content.related_files_list]
    #
    #     # part note
    #     if self.mods.content.part_note and self.mods.content.part_note.text:
    #         data['part'] = self.mods.content.part_note.text
    #
    #     # sublocation
    #     if self.sourcetech.content.sublocation:
    #         data['sublocation'] = self.sourcetech.content.sublocation
    #
    #     # rights access status code
    #     if self.rights.content.access_status:
    #         data['access_code'] = self.rights.content.access_status.code
    #     # copyright date from rights metadata
    #     if self.rights.content.copyright_date:
    #         data['copyright_date'] = self.rights.content.copyright_date
    #     # ip note from rights metadata
    #     if self.rights.content.ip_note:
    #         data['ip_note'] = self.rights.content.ip_note
    #
    #     # boolean values that should always be available
    #     data.update({
    #         # should this item be accessible to researchers?
    #         'researcher_access': bool(self.researcher_access),  # if None, we want False
    #         # flags to indicate which datastreams are available
    #         'has_access_copy': self.compressed_audio.exists,
    #         'has_original': self.audio.exists,
    #     })
    #
    #     if self.compressed_audio.exists:
    #         data.update({
    #             'access_copy_size': self.compressed_audio.info.size,
    #             'access_copy_mimetype': self.compressed_audio.mimetype,
    #     })
    #     if self.digitaltech.content.duration:
    #         data['duration'] = self.digitaltech.content.duration
    #
    #     if self.mods.content.origin_info and \
    #        self.mods.content.origin_info.issued:
    #         data['date_issued'] = [unicode(di) for di in self.mods.content.origin_info.issued]
    #     if self.mods.content.origin_info and \
    #        self.mods.content.origin_info.created:
    #         data['date_created'] = [unicode(di) for di in self.mods.content.origin_info.created]
    #
    #
    #
    #     if self.audio.exists:
    #         data['content_md5'] = self.audio.checksum
    #
    #     return data
    #

    @staticmethod
    def init_from_file(master_filename, initial_label=None, request=None, master_md5_checksum=None,master_sha1_checksum=None,
        master_location=None, master_mimetype=None, access_filename=None, access_location=None, access_md5_checksum=None, access_mimetype=None):
        '''Static method to create a new :class:`Video` instance from
        a file.  Sets the object label and metadata title based on the initial
        label specified, or file basename.  Calculates and stores the duration
        based on the file. Also sets the following default metadata values:

            * mods:typeOfResource = "sound recording"

        :param master_filename: full path to the master file, as a string
        :param initial_label: optional initial label to use; if not specified,
            the base name of the specified file will be used
        :param request: :class:`django.http.HttpRequest` passed into a view method;
            must be passed in order to connect to Fedora as the currently-logged
            in user
        :param master_md5_checksum: the MD5 checksum of the master file being sent to fedora.
        :param master_sha1_checksum: the sha-1 checksum of the master file being sent to fedora.
        :param master_location: optional file URI for file-based Fedora ingest of master file
        :param master_mimetype: the master_mimetype of the master file being sent to fedora
        :param access_filename: full path to the access file, as a string
        :param access_md5_checksum: the MD5 checksum of the access file being sent to fedora.
        :param access_mimetype: the mimetype of the access file being sent to fedora
        :returns: :class:`Video` initialized from the file
        '''

        if initial_label is None:
            initial_label = os.path.basename(master_filename)
        repo = Repository(request=request)
        obj = repo.get_object(type=Video)
        # set initial object label from the base master_filename
        obj.label = initial_label
        obj.dc.content.title = obj.mods.content.title = obj.label
        # Set the file checksum, if set.
        obj.content.checksum = master_md5_checksum
        # set content datastream master_mimetype if passed in
        if master_mimetype is not None:
            obj.content.mimetype = master_mimetype
        #Get the label, minus the extention (master_mimetype indicates that)
        obj.content.label = initial_label.rsplit('.',1)[0]
        # set initial mods:typeOfResource - all Vodeo default to video recording
        obj.mods.content.resource_type = 'video recording'
        # get duration and store in digital tech metadata
        info = MediaInfo.parse(master_filename)
        duration = info.tracks[0].duration / 1000
        obj.digitaltech.content.duration = '%d' % round(duration)

        # premis data
        obj.provenance.content.create_object()
        obj.provenance.content.object.id_type = 'ark'
        obj.provenance.content.object.id = ''

        obj.provenance.content.object.type = 'p:file'
        obj.provenance.content.object.checksums.append(PremisFixity(algorithm='MD5'))
        obj.provenance.content.object.checksums[0].digest = master_md5_checksum

        if master_sha1_checksum is None:
            master_sha1_checksum = sha1sum(master_filename)
        obj.provenance.content.object.checksums.append(PremisFixity(algorithm='SHA-1'))
        obj.provenance.content.object.checksums[1].digest = master_sha1_checksum

        obj.provenance.content.object.create_format()
        #format name will be upper-cased version of file extension
        obj.provenance.content.object.format.name = master_filename.rsplit('.', 1)[1].upper()

        # if a content URI is specified (e.g. for large files), use that
        if master_location is not None:
            obj.content.ds_location = master_location

        # otherwise set the file as content to be posted
        else:
            obj.content.content = open(master_filename)


        # Access copy data

        # if a access URI is specified (e.g. for large files), use that
        if access_location is not None:
            obj.access_copy.ds_location = access_location

        # otherwise set the access file as content to be posted
        else:
            obj.access_copy.content = open(access_filename)

        obj.access_copy.mimetype = access_mimetype
        obj.access_copy.checksum = access_md5_checksum
        obj.access_copy.label = initial_label


        return obj

    @staticmethod
    def init_from_bagit(path, request=None, file_uri=True):
        '''Static method to create a new :class:`Video` instance from
        a BagIt.  Sets the object label and metadata title based on the
        name of the bag, and looks for a supported video file type
        to use as the content datastream for the object.
        Content checksum is pulled from the BagIt metadata, and repository
        ingest will be done via file URIs based on configured
        **LARGE_FILE_STAGING_DIR** and **LARGE_FILE_STAGING_FEDORA_DIR**
        to better support ingesting large files (unless file_uri
        is False).

        Raises an exception if BagIt is not valid or if it does not
        contain a supported video data file.  (Note: using fast validation
        without checksum calculation, to minimize the time required to ingest
        large files.)

        :param path: full path to the BagIt directory that contains
            a video file
        :param request: :class:`django.http.HttpRequest` passed into a view method;
            must be passed in order to connect to Fedora as the currently-logged
            in user
        :param file_uri: ingest BagIt data via file uris based on
            configured staging directories (default behavior)
            instead of uploading the content to Fedora

        :returns: :class:`Video` initialized from the BagIt contents
        '''

        bag = bagit.Bag(path)
        # NOTE: using fast validation here to avoid recalculating checksums
        # for very large files; only checksum compare will be done by fedora
        bag.validate(fast=True)  # raises bagit.BagValidationError if not valid

        # use the base name of the BagIt as initial object label
        initial_label = os.path.basename(path)

        # identify video content file within the bag
        m = magic.Magic(mime=True)
        # loop through bag content until we find a supported video file

        opts = {'request': request, 'initial_label' : initial_label}

        for data_path in bag.payload_files():
            # path is relative to bag root dir
            filename = os.path.join(path, data_path)
            mtype = m.from_file(filename)
            mimetype, separator, options = mtype.partition(';')

            # require both MD5 and SHA-1 for video to ingest
            try:
                md5_checksum = bag.entries[data_path]['md5']
            except KeyError:
                raise Exception('MD5 checksum mismatch on file %s' % data_path)
            try:
                sha1_checksum = bag.entries[data_path]['sha1']
            except KeyError:
                raise Exception('SHA-1 checksum mismatch on file %s' % data_path)

            if mimetype in Video.allowed_master_mimetypes:
                opts['master_filename'] = filename
                opts['master_md5_checksum'] = md5_checksum
                opts['master_sha1_checksum'] = sha1_checksum
                opts['master_mimetype'] = mimetype
                if file_uri:
                    # if Fedora base path is different from locally mounted staging directory,
                    # convert from local path to fedora server path
                    master_location = 'file://%s' % urllib.quote(opts['master_filename'])
                    if getattr(settings, 'LARGE_FILE_STAGING_FEDORA_DIR', None) is not None:
                        master_location = master_location.replace(settings.LARGE_FILE_STAGING_DIR,
                            settings.LARGE_FILE_STAGING_FEDORA_DIR)
                    opts['master_location'] = master_location

            elif mimetype in Video.allowed_access_mimetypes:
                opts['access_filename'] = filename
                opts['access_md5_checksum'] = md5_checksum
                opts['access_mimetype'] = mimetype
                if file_uri:
                    # if Fedora base path is different from locally mounted staging directory,
                    # convert from local path to fedora server path
                    access_location = 'file://%s' % urllib.quote(opts['access_filename'])
                    if getattr(settings, 'LARGE_FILE_STAGING_FEDORA_DIR', None) is not None:
                        access_location = access_location.replace(settings.LARGE_FILE_STAGING_DIR,
                            settings.LARGE_FILE_STAGING_FEDORA_DIR)
                    opts['access_location'] = access_location
        # no Video found
        if 'master_filename' not in opts:
            raise Exception('No Video content found in %s' % os.path.basename(path))

        vid = Video.init_from_file(**opts)
                                   
        return vid

    #
    # @staticmethod
    # def all():
    #     'Find all Audio objects by content model within the configured pidspace.'
    #     search_opts = {
    #         'type': AudioObject,
    #         # restrict to objects in configured pidspace
    #         'pid__contains': '%s:*' % settings.FEDORA_PIDSPACE,
    #         # restrict by cmodel in dc:format
    #         'format__contains': AudioObject.AUDIO_CONTENT_MODEL,
    #     }
    #     repo = Repository()
    #     return repo.find_objects(**search_opts)

