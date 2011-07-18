from collections import namedtuple
from datetime import date
import os
import wave
import logging
import mutagen
import math
import tempfile

from rdflib import URIRef
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import permalink

from eulxml import xmlmap
from eullocal.django.taskresult.models import TaskResult
from eulfedora.models import FileDatastream, XmlDatastream
from eulfedora.rdfns import relsext
from eulfedora.util import RequestFailed

from keep.collection.models import CollectionObject
from keep.common.fedora import DigitalObject, Repository, LocalMODS
from keep import mods

logger = logging.getLogger(__name__)

##
## MODS
##

class AudioMods(LocalMODS):
    '''Customized MODS for :class:`AudioObject`, based on
    :class:`~keep.common.fedora.LocalMODS`.'''
    # possibly map identifier type uri as well ?
    general_note = xmlmap.NodeField('mods:note[@type="general"]',
          mods.TypedNote, required=False)
    ':class:`~keep.mods.TypedNote` with `type="general"`'
    part_note = xmlmap.NodeField('mods:note[@type="part number"]',
                                 mods.TypedNote)
    ':class:`~keep.mods.TypedNote` with `type="part number"`'

    dm1_abstract_note = xmlmap.NodeField('mods:note[@type="dm1_abstract"]',
            mods.TypedNote, required=False, verbose_name='DM Abstract')
    dm1_content_note = xmlmap.NodeField('mods:note[@type="dm1_content_notes"]',
            mods.TypedNote, required=False, verbose_name='DM Content Notes')
    dm1_toc_note = xmlmap.NodeField('mods:note[@type="dm1_toc"]',
            mods.TypedNote, required=False, verbose_name='DM Table of Contents')
    dm1_id = xmlmap.StringField('mods:identifier[@type="dm1_id"]',
            required=False, verbose_name='Record ID/Filename')
    dm1_other_id = xmlmap.StringField('mods:identifier[@type="dm1_other"]',
            required=False, verbose_name='Other ID')

##
## Source technical metadata
##

class _BaseSourceTech(xmlmap.XmlObject):
    'Base class for Source Technical Metadata objects'
    ROOT_NS = 'http://pid.emory.edu/ns/2010/sourcetech'
    ROOT_NAMESPACES = {'st': ROOT_NS }

class SourceTechMeasure(_BaseSourceTech):
    ''':class:`~eulxml.xmlmap.XmlObject` for :class:`SourceTech` measurement
    information'''
    ROOT_NAME = 'measure'
    unit = xmlmap.StringField('@unit')
    'unit of measurement'
    aspect = xmlmap.StringField('@aspect')
    'aspect of measurement'
    value = xmlmap.StringField('text()')
    'value (actual measurement)'

    def is_empty(self):
        '''Returns False if no measurement value is set; returns True if any
        measurement value is set.  Attributes are ignored for determining whether
        or not the field should be considered empty, since aspect & unit
        are only meaningful in reference to an actual measurement value.'''
        return not self.node.text

class SourceTech(_BaseSourceTech):
    ':class:`~eulxml.xmlmap.XmlObject` for Source Technical Metadata.'
    ROOT_NAME = 'sourcetech'

    # option lists for controlled vocabulary source tech fields
    form_options = ('', 'audio cassette', 'open reel tape', 'LP', 'CD', 'sound file (WAV)',
        'sound file (MP3)', 'sound file (M4A)', 'sound file (AIFF)', 'microcassette',
        'DAT', '78', '45 RPM', 'acetate disc', 'aluminum disc', 'glass disc',
        'flexi disc', 'cardboard disc', 'phonograph cylinder', 'wire recording',
        'dictabelt', 'other')
    'controlled vocabulary for :class:`SourceTech.form`'
    housing_options = ('', 'jewel case', 'plastic container', 'paper sleeve',
        'cardboard sleeve', 'cardboard box', 'other', 'none')
    'controlled vocabulary for :class:`SourceTech.housing`'
    reel_sizes = ('3', '4', '5', '7', '10', '12', '14') # also Other -> empty field
    'controlled vocabulary used to generate form options for :class:`SourceTech.reel_size`'
    reel_size_options = [(size, '%s"' % size) for size in reel_sizes]
    reel_size_options.append(('Other', 'Other'))
    reel_size_options.append(('Not Applicable', 'Not Applicable'))
    # add an empty value at the beginning of the list to force active selection
    reel_size_options.insert(0, ('', ''))
    sound_characteristic_options = ('', 'mono', 'stereo')
    'controlled vocabulary for :class:`SourceTech.sound_characteristics`'
    speed_options = (
        # delimited format is aspect, value, unit
        ('', ''),
        ('tape', (
            ('tape|15/16|inches/sec', '15/16 ips'),
            ('tape|1.2|cm/sec', '1.2 cm/s'),
            ('tape|1 7/8|inches/sec', '1 7/8 ips'),
            ('tape|2.4|cm/sec', '2.4 cm/s'),
            ('tape|3 3/4|inches/sec', '3 3/4 ips'),
            ('tape|7 1/2|inches/sec', '7 1/2 ips'),
            ('tape|15|inches/sec', '15 ips'),
            ('tape|30|inches/sec', '30 ips'),
            ('tape|other|other', 'Other'),
            )
         ),
        ('phono disc', (
            ('phono disc|16|rpm', '16 rpm'),
            ('phono disc|33 1/3|rpm', '33 1/3 rpm'),
            ('phono disc|45|rpm', '45 rpm'),
            ('phono disc|78|rpm', '78 rpm'),
            ('phono disc|other|other', 'Other'),
            )
        ),
        ('phono cylinder', (
            ('phono cylinder|90|rpm', '90 rpm'),
            ('phono cylinder|120|rpm', '120 rpm'),
            ('phono cylinder|160|rpm', '160 rpm'),
            ('phono cylinder|other|other', 'Other'),
            ),
        ),
        ('other', (
            ('other|other|other', 'Other'),
            ),
        ),
        ('na|Not applicable|na', 'Not Applicable'),
    )
    'controlled vocabulary for :class:`SourceTech.speed`, grouped by format'
    # NOTE: speed should be displayed as ips but saved to xml as inches/sec
    # speed options is formatted for grouped options in django select widget

    # planned schema location (schema not yet available)
    #XSD_SCHEMA = 'http://pid.emory.edu/ns/2010/sourcetech/v1/sourcetech-1.xsd'
    #xmlschema = xmlmap.loadSchema(XSD_SCHEMA)
    note = xmlmap.StringField('st:note[@type="general"]', required=False,
        verbose_name='General Note', help_text='General note about the physical item')
    'general note'
    note_list = xmlmap.StringListField('st:note[@type="general"]')
    related_files = xmlmap.StringField('st:note[@type="relatedFiles"]', required=False,
        help_text='IDs of other digitized files for the same item, separated by semicolons. Required for multi-part items.')
    'related files (string of IDs delimited by semicolons'
    related_files_list = xmlmap.StringListField('st:note[@type="relatedFiles"]')
        # NOTE: according to spec, related_files is required if multi-part--
        # - not tracking multi-part for Min Items (that I know of)
    conservation_history = xmlmap.StringField('st:note[@type="conservationHistory"]',
        required=False)
    'note about conservation history'
    conservation_history_list = xmlmap.StringListField('st:note[@type="conservationHistory"]')
    speed = xmlmap.NodeField('st:speed/st:measure[@type="speed"]',
        SourceTechMeasure)
    ':class:`SourceTechMeasure`'
    sublocation = xmlmap.StringField('st:sublocation', required=False,
        help_text='Storage location within the collection (e.g., box and folder)')
    'storage location within the collection'
    form = xmlmap.StringField('st:form[@type="sound"]', choices=form_options,
        required=False, help_text='The physical form or medium of the resource')
    'physical format - options controlled by :class:`SourceTech.form_options`'
    form_list = xmlmap.StringListField('st:form[@type="sound"]')
    sound_characteristics = xmlmap.StringField('st:soundChar',
        choices=sound_characteristic_options, required=False)
    'sound characteristics - options controlled by :class:`SourceTech.sound_characteristic_options`'
    stock = xmlmap.StringField('st:stock', verbose_name='Tape Brand/Stock',
       help_text='The brand or stock of the magnetic tape', required=False)
    'Stock or brand of source media'
    stock_list = xmlmap.StringListField('st:stock')
    housing = xmlmap.StringField('st:housing[@type="sound"]', choices=housing_options,
        help_text='Type of housing for the source item')
    'Type of housing - options controlled by :class:`SourceTech.housing_options`'
    reel_size =  xmlmap.NodeField('st:reelSize/st:measure[@type="diameter"][@aspect="reel size"]',
            SourceTechMeasure, required=False)
    ':class:`SourceTechMeasure`'
    # tech_note is migrate/view only
    technical_note = xmlmap.StringListField('st:note[@type="technical"]', required=False)
    'note with type="technical"'


##
## Digital technical metadata
##

class _BaseDigitalTech(xmlmap.XmlObject):
    'Base class for Digital Technical Metadata objects'
    ROOT_NS = 'http://pid.emory.edu/ns/2010/digitaltech'
    ROOT_NAMESPACES = {'dt': ROOT_NS }

class TransferEngineer(_BaseDigitalTech):
    ''':class:`~eulxml.xmlmap.XmlObject` for :class:`DigitalTech` transfer engineer'''
    ROOT_NAME = 'transferEngineer'
    id = xmlmap.StringField('@id')
    'unique id to identify the transfer engineer'
    id_type = xmlmap.StringField('@idType')
    'type of id used'
    name = xmlmap.StringField('text()')
    'full display name for the transfer engineer'

    LDAP_ID_TYPE = 'ldap'
    DM_ID_TYPE = 'dm1'
    LOCAL_ID_TYPE = 'local'
    
    local_engineers = {
        'vendor1': 'Vendor',
        'other1': 'Other',
    }

class CodecCreator(_BaseDigitalTech):
    ''':class:`~eulxml.xmlmap.XmlObject` for :class:`DigitalTech` codec creator'''
    ROOT_NAME = 'codecCreator'
    configurations = {
        # current format is     id :  hardware, software, software version
        '1': ( ('Mac G4',), 'DigiDesign ProTools LE',  '5.2'),
        '2': ( ('Mac G5',), 'DigiDesign ProTools LE',  '6.7'),
        '3': (('Dell Optiplex 755', 'Apogee Rosetta 200'), 'Sound Forge',  '9.0'),
        '4': (('Dell Optiplex 755',), 'iTunes',  None),
        '5': (('Unknown',), 'Unknown',  None),
    }
    'controlled vocabulary for codec creator configurations'
    options = [(id, '%s, %s %s' % (', '.join(c[0]), c[1], c[2] if c[2] is not None else ''))
                    for id, c in configurations.iteritems()]
    options.insert(0, ('', '')) # empty value at beginning of list (initial default)

    id = xmlmap.StringField('dt:codecCreatorID')
    'codec creator id - `dt:codecCreatorId`'
    hardware = xmlmap.StringField('dt:hardware')
    'hardware  - `dt:hardware` (first hardware only, even if there are multiple)'
    hardware_list = xmlmap.StringListField('dt:hardware')
    'list of all hardware'
    software = xmlmap.StringField('dt:software')
    'software  - `dt:software` (first software only, even if there are multiple)'
    software_version = xmlmap.StringField('dt:softwareVersion')
    'list of all software'

class DigitalTech(_BaseDigitalTech):
    ":class:`~eulxml.xmlmap.XmlObject` for Digital Technical Metadata."
    ROOT_NAME = 'digitaltech'
    date_captured = xmlmap.StringField('dt:dateCaptured[@encoding="w3cdtf"]',
        help_text='Date digital capture was made', required=True)
    'date digital capture was made (string)'
    codec_quality = xmlmap.StringField('dt:codecQuality', required=True,
        help_text='Whether the data compression method was lossless or lossy')
    'codec quality - lossless or lossy'
    duration = xmlmap.IntegerField('dt:duration/dt:measure[@type="time"][@unit="seconds"][@aspect="duration of playing time"]',
        help_text='Duration of audio playing time', required=True)
    'duration of the audio file'
    # FIXME/TODO: note and digitization purpose could be plural
    note = xmlmap.StringField('dt:note[@type="general"]', required=False,
        help_text='Additional information that may be helpful in describing the surrogate')
    'general note'
    note_list = xmlmap.StringListField('dt:note[@type="general"]')
    digitization_purpose = xmlmap.StringField('dt:note[@type="purpose of digitization"]',
        required=False,
        help_text='The reason why the digital surrogate was created (e.g., exhibit, patron request, preservation)')
    'reason the item was digitized'
    digitization_purpose_list = xmlmap.StringListField('dt:note[@type="purpose of digitization"]')
    transfer_engineer = xmlmap.NodeField('dt:transferEngineer', TransferEngineer,
        required=False, help_text='The person who performed the digitization or conversion that produced the file')
    ':class:`TransferEngineer` - person who digitized the item'
    codec_creator = xmlmap.NodeField('dt:codecCreator', CodecCreator,
        help_text='Hardware, software, and software version used to create the digital file')
    ':class:`CodecCreator` - hardware & software used to digitize the item'


##
## Rights
##

class _BaseRights(xmlmap.XmlObject):
    'Base class for Rights metadata objects'
    ROOT_NS = 'http://pid.emory.edu/ns/2010/rights'
    ROOT_NAMESPACES = { 'rt': ROOT_NS }

class AccessStatus(_BaseRights):
    ':class:`~eulxml.xmlmap.XmlObject` for :class:`Rights` access status'
    ROOT_NAME = 'accessStatus'
    code = xmlmap.StringField('@code', required=True)
    'access code'
    text = xmlmap.StringField('text()')
    'text description of rights access code'

_access_term = namedtuple('_access_term', 'code abbreviation access text') # wraps terms below
class Rights(_BaseRights):
    'Rights metadata'
    ROOT_NAME = 'rights'

    access_terms = (
        # code  abbreviation                     file access allowed?        (full description next line)
        ('1', 'C108-a donor request',              False,     # metadata ok
            'Material under copyright; digital copy made under Section 108a, per donor/ copyright holder request'),
        ('2', 'C108-b or c',                       True,
            'Material under copyright; digital copy made under Section 108b or c; no explicit contract restrictions in the donor agreement'),
        ('3', 'C108-b or c + MARBL use',           True,
            'Material under copyright; digital copy made under Section 108b or c; permission received from copyright holder for Emory University Libraries to use digitized copy in public display, exhibition, etc.'),
        ('4', 'C108-b or c + donor restriction',   False,
            'Material under copyright; digital copy made under Section 108b or c; restriction on item per donor agreement'),
        ('5', 'C108-b or c + Emory Restriction',   False,
            'Material under copyright; digital copy made under Section 108b or c; restriction on item per Emory University Libraries'),
        ('6', 'C held Emory U',                    True,
            'Material under copyright; Emory University holds copyright'),
        ('7', 'C trans to Emory U',                True,
            'Material under copyright; copyright transferred to Emory University'),
        ('8', 'Public Domain',                     True,
            'Material is in public domain'),
        ('9', 'PD - Restricted by Donor or MARBL', False,
            'Material is in public domain; restriction on item per a non-copyright reason in the donor agreement or by Emory University Libraries'),
        ('10', 'Undetermined',                     False,     # metadata ok
            'Access status undetermined'),
        ('11', 'Unknown from Old DM',              True,
            'Material from previous Digital Masters database that cannot be mapped to other codes'),
    ) 
    '''controlled vocabulary for access condition, ordered the way they should
    appear on the form widget'''

    access_terms_dict = dict((term[0], _access_term(*term))
                             for term in access_terms)
    '''dictionary mapping access_terms codes to access term objects. Each
    access term object has three properties: code, abbreviation, access, and text, which
    map to elements of access_terms.'''
    # e.g., access_terms_dict['11'].access == True

    access_status = xmlmap.NodeField('rt:accessStatus', AccessStatus,
        required=True,
        help_text='File access status, as determined by analysis of copyright, donor agreements, permissions, etc.')
    ':class:`AccessStatus`'
    copyright_holder_name = xmlmap.StringField('rt:copyrightholderName',
        required=False,
        help_text='Name of a copyright holder in last, first order')
    'name of the copyright holder'
    copyright_date = xmlmap.StringField('rt:copyrightDate[@encoding="w3cdtf"]',
        required=False,
        help_text='Date of copyright')
    'copyright date (string)'

    block_external_access = xmlmap.SimpleBooleanField('rt:externalAccess',
        'deny', None,
        help_text='''DENY ACCESS to library patrons irrespective of Access Status.''')
    '''block external access. If this is True then refuse patron access to this
    item irrespective of :attr:access_status.'''
    # NOTE: users have also requested a <rt:externalAccess>allow</rt:externalAccess>
    # to allow access irrespective of access_status. when we implement
    # that, we'll probably want to incorporate it into this property and
    # rename

    ip_note = xmlmap.StringField('rt:ipNotes', required=False, verbose_name='IP Note',
        help_text='Additional information about the intellectual property rights of the associated work.')
    # NOTE: eventually should be repeatable/StringListField

    @property
    def researcher_access(self):
        '''Does this rights XML indicate that researchers should be
        allowed access to this document?'''
        if self.block_external_access:
            return False

        if not self.access_status:
            return None
        access_code = self.access_status.code
        access_term = self.access_terms_dict.get(access_code, None)
        if not access_term:
            return None

        return access_term.access


##
## Fedora AudioObject
##

class AudioObject(DigitalObject):
    '''Fedora Audio Object.  Extends :class:`~eulfedora.models.DigitalObject`.'''
    AUDIO_CONTENT_MODEL = 'info:fedora/emory-control:EuterpeAudio-1.0'
    CONTENT_MODELS = [ AUDIO_CONTENT_MODEL ]
    NEW_OBJECT_VIEW = 'audio:view'

    mods = XmlDatastream("MODS", "MODS Metadata", AudioMods, defaults={
            'control_group': 'M',
            'format': mods.MODS_NAMESPACE,
            'versionable': True,
        })
    'MODS :class:`~eulfedora.models.XmlDatastream` with content as :class:`AudioMods`'

    audio = FileDatastream("AUDIO", "Audio datastream", defaults={
            'mimetype': 'audio/x-wav',
            'versionable': True,
        })
    'master audio :class:`~eulfedora.models.FileDatastream`'

    compressed_audio = FileDatastream("CompressedAudio", "Compressed audio datastream", defaults={
            'mimetype': 'audio/mpeg',
            'versionable': True,
        })
    'access copy of audio :class:`~eulfedora.models.FileDatastream`'

    digitaltech = XmlDatastream("DigitalTech", "Technical Metadata - Digital", DigitalTech,
        defaults={
            'control_group': 'M',
            'versionable': True,
        })
    '''digital technical metadata :class:`~eulfedora.models.XmlDatastream`
    with content as :class:`DigitalTech`'''

    sourcetech = XmlDatastream("SourceTech", "Technical Metadata - Source", SourceTech,
        defaults={
            'control_group': 'M',
            'versionable': True,
        })
    '''source technical metadata :class:`~eulfedora.models.XmlDatastream` with content as
    :class:`SourceTech`'''

    rights = XmlDatastream("Rights", "Usage rights and access control metadata", Rights,
        defaults={
            'control_group': 'M',
            'versionable': True,
        })
    '''access control metadata :class:`~eulfedora.models.XmlDatastream`
    with content as :class:`Rights`'''

    _collection_uri = None

    def save(self, logMessage=None):
        '''Save the object.  If the content of any :class:`~AudioObject.mods`,
        :class:`AudioObject.rels_ext`, or :class:`AudioObject.digitaltech`
        datastreams have been changed, the DC will be updated and saved as well.

        :param logMessage: optional log message
        '''
        if not self.exists or self.mods.isModified() or self.rels_ext.isModified or \
            self.digitaltech.isModified():
            # DC is derivative metadata based on MODS/RELS-EXT/Digital Tech
            # If this is a new item (does not yet exist in Fedora)
            # OR if any of the relevant datastreams have changed, update DC
            self._update_dc()

        # for now, keep object label in sync with MODS title
        if self.mods.isModified() and self.mods.content.title:
            self.label = self.mods.content.title

        return super(AudioObject, self).save(logMessage)

    @permalink
    def get_absolute_url(self):
        'Absolute url to view this object within the site'
        return ('audio:view', [str(self.pid)])

    def get_access_url(self):
        "Absolute url to hear this object's access version"
        if self.compressed_audio.exists:
            return reverse('audio:download-compressed-audio', args=[str(self.pid)])

        # otherwise see if it's from old dm
        old_dm_path = self.old_dm_media_path()
        if old_dm_path:
            old_dm_root = getattr(settings, 'OLD_DM_MEDIA_ROOT', '')
            return old_dm_root + old_dm_path

    def old_dm_media_path(self):
        old_id = self.mods.content.dm1_other_id or self.mods.content.dm1_id
        if old_id:
            coll_obj = self._collection_object()
            if not coll_obj:
                return
            coll_path = coll_obj.old_dm_media_path()
            if not coll_path:
                return
            return '%saudio/%s.m4a' % (coll_path, old_id)

    def _collection_object(self):
        repo = Repository()
        coll_uri = self.collection_uri
        if coll_uri:
            return repo.get_object(coll_uri, type=CollectionObject)

    @property
    def conversion_result(self):
        '''Return the :class:`~eullocal.django.taskresult.models.TaskResult`
        for the most recently requested access copy conversion (if any).
        '''
        conversions = TaskResult.objects.filter(object_id=self.pid).order_by('-created')
        if conversions:
            return conversions[0]

    @property
    def researcher_access(self):
        return self.rights.content.researcher_access

    def _update_dc(self):
        '''Update Dublin Core (derivative metadata) based on master metadata
        from MODS, RELS-EXT, and digital tech metadata in order to keep data
        synchronized and make fields that need to be searchable accessible to
        Fedora findObjects API method.
         '''
        # identifiers
        del(self.dc.content.identifier_list)        # clear out any existing names
        
        # title
        if self.mods.content.title:
            self.label = self.mods.content.title
            self.dc.content.title = self.mods.content.title
        if self.mods.content.resource_type:
            self.dc.content.type = self.mods.content.resource_type

        # creator names
        del(self.dc.content.creator_list)        # clear out any existing names
        for name in self.mods.content.names:
            # for now, use unicode conversion as defined in mods.Name
            self.dc.content.creator_list.append(unicode(name))

        # clear out any dates previously in DC
        del(self.dc.content.date_list)        
        if self.mods.content.origin_info and \
           len(self.mods.content.origin_info.created) and \
           self.mods.content.origin_info.created[0].date:
            self.dc.content.date_list.append(self.mods.content.origin_info.created[0].date)
        if self.mods.content.origin_info and \
           len(self.mods.content.origin_info.issued) and \
           self.mods.content.origin_info.issued[0].date:
            self.dc.content.date_list.append(self.mods.content.origin_info.issued[0].date)

        # clear out any descriptions previously in DC and set from MODS/digitaltech
        del(self.dc.content.description_list)
        if self.mods.content.general_note and \
           self.mods.content.general_note.text:
            self.dc.content.description_list.append(self.mods.content.general_note.text)

        # clear out any rights previously in DC and set contents from Rights accessStatus
        del(self.dc.content.rights_list)
        if self.rights.content.access_status:
            # access code no longer needs to be included, since we will not be searching
            self.dc.content.rights_list.append(self.rights.content.access_status.text)


    def index_data(self):
        '''Extend the default
        :meth:`eulfedora.models.DigitalObject.index_data`
        method to include additional fields specific to Keep
        Audio objects.'''
        # NOTE: we don't want to rely on other objects being indexed in Solr,
        # so index data should not use Solr to find any related object info


        # FIXME: is it worth splitting out descriptive index data here?
        data = super(AudioObject, self).index_data()
        if self.collection_uri is not None:
            data['collection_id'] = self.collection_uri
            try:
                # pull parent & archive collection objects directly from fedora
                parent = CollectionObject(self.api, self.collection_uri)
                data['collection_label'] = parent.label
                # the parent collection of the collection this item belongs to is its archive
                # FIXME: CollectionObject uses collection_id where AudioObject uses collection_uri
                data['archive_id'] = parent.collection_id
                archive = CollectionObject(self.api, parent.collection_id)
                data['archive_label'] = archive.label
            except RequestFailed as rf:
                logger.error('Error accessing collection or archive object in Fedora: %s' % rf)

        # include resolvable ARK if available
        if self.mods.content.ark_uri:
            data['ark_uri'] =  self.mods.content.ark_uri
            
        # old identifiers from previous digital masters
        dm1_ids = []
        if self.mods.content.dm1_id:
            dm1_ids.append(self.mods.content.dm1_id)
        if self.mods.content.dm1_other_id:
            dm1_ids.append(self.mods.content.dm1_other_id)
        if dm1_ids:
            data['dm1_id'] = dm1_ids

        # digitization purpose, if not empty
        if self.digitaltech.content.digitization_purpose_list:
            # convert nodelist to a normal list that can be serialized as json
            data['digitization_purpose'] = [dp for dp in self.digitaltech.content.digitization_purpose_list]

        # related files
        if self.sourcetech.content.related_files_list:
            data['related_files'] = [rel for rel in self.sourcetech.content.related_files_list]

        # part note 
        if self.mods.content.part_note and self.mods.content.part_note.text:
            data['part'] = self.mods.content.part_note.text

        # rights access status code
        if self.rights.content.access_status:
            data['access_code'] = self.rights.content.access_status.code

        # boolean values that should always be available
        data.update({
            # should this item be accessible to researchers?
            'researcher_access': bool(self.researcher_access),  # if None, we want False
            # flags to indicate which datastreams are available
            'has_access_copy': self.compressed_audio.exists,
            'has_original': self.audio.exists,
        })

        if self.compressed_audio.exists:
            data.update({
                'access_copy_size': self.compressed_audio.info.size,
                'access_copy_mimetype': self.compressed_audio.mimetype,
	    })
        if self.digitaltech.content.duration:
            data['duration'] = self.digitaltech.content.duration
            
        if self.mods.content.origin_info and \
           self.mods.content.origin_info.issued:
            data['date_issued'] = [unicode(di) for di in self.mods.content.origin_info.issued]
            
        return data


    @staticmethod
    def init_from_file(filename, initial_label=None, request=None, checksum=None):
        '''Static method to create a new :class:`AudioObject` instance from
        a file.  Sets the object label and metadata title based on the initial
        label specified, or file basename.  Calculates and stores the duration
        based on the file. Also sets the following default metadata values:
        
            * mods:typeOfResource = "sound recording"
            * dt:codecQuality = "lossless"

        :param filename: full path to the audio file, as a string
        :param initial_label: optional initial label to use; if not specified,
            the base name of the specified file will be used
        :param request: :class:`django.http.HttpRequest` passed into a view method;
            must be passed in order to connect to Fedora as the currently-logged
            in user
        :param checksum: the checksum of the file being sent to fedora.
        :returns: :class:`AudioObject` initialized from the file
        '''
        if initial_label is None:
            initial_label = os.path.basename(filename)
        repo = Repository(request=request)
        obj = repo.get_object(type=AudioObject)
        # set initial object label from the base filename
        obj.label = initial_label
        obj.dc.content.title = obj.mods.content.title = obj.label
        obj.audio.content = open(filename)  # FIXME: at what point does/should this get closed?
        #Set the file checksum, if set.
        obj.audio.checksum=checksum
        #Get the label, minus the ".wav" (mimetype indicates that)
        obj.audio.label = initial_label[:-4]
        # set initial mods:typeOfResource - all AudioObjects default to sound recording
        obj.mods.content.resource_type = 'sound recording'
        # set codec quality to lossless in digital tech metadata 
        # - default for AudioObjects, should only accept lossless audio for master file
        obj.digitaltech.content.codec_quality = 'lossless'
        # get wav duration and store in digital tech metadata
        obj.digitaltech.content.duration = '%d' % round(wav_duration(filename))

        return obj

    def _get_collection_uri(self):
        # for now, an audio object should only have one isMemberOfCollection relation
        if self._collection_uri is None:
            self._collection_uri = self.rels_ext.content.value(
                        subject=self.uriref,
                        predicate=relsext.isMemberOfCollection)
        return self._collection_uri

    def _set_collection_uri(self, collection_uri):
        # TODO: handle None!!!  don't set to rdflib.term.URIRef('None')), clear out rels-ext
        if collection_uri is None:

            # remove the current collection membership 
            self.rels_ext.content.remove((
                self.uriref,
                relsext.isMemberOfCollection,
                self._collection_uri))
            
            # clear out any cached collection id
            self._collection_uri = None

        else:
            if not isinstance(collection_uri, URIRef):
                collection_uri = URIRef(collection_uri)

            # update/replace any existing collection membership (only one allowed, for now)
            self.rels_ext.content.set((
                self.uriref,
                relsext.isMemberOfCollection,
                collection_uri))
            # clear out any cached collection id
            self._collection_uri = None

    # FIXME: CollectionObject has an equivalent property called
    # collection_id; should these be consisent? common code?
    collection_uri = property(_get_collection_uri, _set_collection_uri)
    ':class:`~rdflib.URIRef` for the collection this object belongs to'

    @staticmethod
    def all():
        'Find all Audio objects by content model within the configured pidspace.'
        search_opts = {
            'type': AudioObject,
            # restrict to objects in configured pidspace
            'pid__contains': '%s:*' % settings.FEDORA_PIDSPACE,
            # restrict by cmodel in dc:format
            'format__contains': AudioObject.AUDIO_CONTENT_MODEL,
        }
        repo = Repository()
        return repo.find_objects(**search_opts)


def wav_duration(filename):
    """Calculate the duration of a WAV file using Python's built in :mod:`wave`
    library.  Raises a StandardError if file cannot be read as a WAV.

    :param filename: full path to the WAV file
    :returns: duration in seconds as a float
    """
    try:
        wav_file = wave.open(filename, 'rb')
    except wave.Error as werr:
        # FIXME: is there a better/more specific exception that can be used here?
        raise StandardError('Failed to open file %s as a WAV due to: %s' % (filename, werr))
    # any other file errors will be propagated as IOError
    
    # duration in seconds = number of samples / sampling frequency
    duration = float(wav_file.getnframes())/float(wav_file.getframerate())
    return duration

def check_wav_mp3_duration(obj_pid=None,wav_file_path=None,mp3_file_path=None):
    '''Compare the durations of a wav file with an mp3 file (presumably an mp3
    generated from the wav via :meth:`keep.audio.tasks.convert_wav_to_mp3` )
    to check that they are roughly the same length.

    :param obj_pid: The pid of a fedora object (expected to be an
	AudioObject) to get the wav and/or mp3 files from if they are
        not specified by path.

    :param wav_file_path: Path to the wav_file to use for comparison;
    	if not specified, it will be downloaded from the object in
        Fedora.
      
    :param mp3_file_path: Path to the mp3_file to use for comparison;
    	if not specified, it will be downloaded from the object in
    	Fedora.  Note that this file must end in .mp3 for the duration
        to be calculated.
                          
    :returns: True if the two files have the same duration, or close
	enough duration (no more than 1 second difference)
    '''
    try:
        #Initialize temporary files to None.
        tmp_wav_path = None
        tmp_mp3_path = None

        #Initialize connection to the repository:
        repo = Repository()

        #Using the ingest directory to simplify cleanup in case extra files hang around.
        tempdir = settings.INGEST_STAGING_TEMP_DIR
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)

        #If no wav file is specified, use the object.
        if wav_file_path is None:
            #Load the object.
            obj = repo.get_object(obj_pid, type=AudioObject)
            # download the compressed audio file from the object in fedora
            # mkstemp returns file descriptor and full path to the temp file
            tmp_fd_wav, tmp_wav_path = tempfile.mkstemp(dir=tempdir,suffix=".mp3")       
            try:
                destination = os.fdopen(tmp_fd_wav, 'wb+')
            except Exception as e:
                os.close(tmp_fd_wav)
                raise
            
            try:
                 destination.write(obj.audio.content.read())
            except Exception as e:                
                 raise
            finally:
                # NOTE: This automatically closes the open tmpfd via Python magic;
                # calling os.close(tmpfd) at this point will error.
                destination.close()
        #Else use the passed in wav file.
        else:
            tmp_wav_path = wav_file_path

        #If no mp3 file is specified, use the object.
        if mp3_file_path is None:
            #Load the object.
            obj = repo.get_object(obj_pid, type=AudioObject)
            #Verify the compressed datastream exists, if not, return false as cannot match.
            if(not obj.compressed_audio.exists):
                return False

            # download the master audio file from the object in fedora
            # mkstemp returns file descriptor and full path to the temp file
            tmp_fd_mp3, tmp_mp3_path = tempfile.mkstemp(dir=tempdir,suffix=".mp3")
            try:
                destination = os.fdopen(tmp_fd_mp3, 'wb+')
            except Exception:
                os.close(tmp_fd_mp3)
                raise
            
            try:
                destination.write(obj.compressed_audio.content.read())
            # just pass any exceptions up the chain
            finally:
                # NOTE: This automatically closes the open tmpfd via Python magic;
                # calling os.close(tmpfd) at this point will error.
                destination.close()
        #Else use the passed in wav file.
        else:
            tmp_mp3_path = mp3_file_path

        #Get information on the mp3 file using mutagen:
        mp3_tags = mutagen.File(tmp_mp3_path)
        if mp3_tags is None:
            raise Exception('Could not get MP3 tag information for MP3 file %s' % tmp_mp3_path)
            
        mp3_length = mp3_tags.info.length
        wav_length = wav_duration(tmp_wav_path)

        #Verify the wav file and the mp3 file are the same length to within 1.0 seconds.
        return (math.fabs(mp3_length - wav_length) < 1.0)
    except Exception:
        raise
    #Cleanup for everything.
    finally:
        # Only remove wav if file was not passed in (ie. only remove the temporary file).
        if wav_file_path is None and tmp_wav_path is not None:
            if os.path.exists(tmp_wav_path):
                os.remove(tmp_wav_path)

        # Only remove mp3 if file was not passed in (ie. only remove the temporary file).
        if mp3_file_path is None and tmp_mp3_path is not None:
            if os.path.exists(tmp_mp3_path):
                os.remove(tmp_mp3_path)
