import os
from rdflib import URIRef
import wave

from eulcore import xmlmap
from eulcore.fedora.models import FileDatastream, XmlDatastream
from eulcore.fedora.rdfns import relsext

from digitalmasters.fedora import DigitalObject, Repository
from digitalmasters import mods


class AudioMods(mods.MODS):
    """AudioObject-specific MODS, based on :class:`mods.MODS`."""
    # possibly map identifier type uri as well ?
    general_note = xmlmap.NodeField('mods:note[@type="general"]',
          mods.Note, instantiate_on_get=True, required=False)
    part_note = xmlmap.NodeField('mods:note[@type="part number"]',
                                          mods.Note, instantiate_on_get=True)

class _BaseSourceTech(xmlmap.XmlObject):
    'Base class for Source Technical Metadata objects'
    ROOT_NS = 'http://pid.emory.edu/ns/2010/sourcetech'
    ROOT_NAMESPACES = {'st': ROOT_NS }

class SourceTechMeasure(_BaseSourceTech):
    ROOT_NAME = 'measure'
    unit = xmlmap.StringField('@unit')
    aspect = xmlmap.StringField('@aspect')
    value = xmlmap.StringField('.')

class SourceTech(_BaseSourceTech):
    'Source Technical Metadata'
    ROOT_NAME = 'sourcetech'

    # option lists for controlled vocabulary source tech fields
    form_options = ('audio cassette', 'open reel tape', 'LP', 'CD', 'sound file (WAV)',
        'sound file (MP3)', 'sound file (M4A)', 'sound file (AIFF)', 'microcassette',
        'DAT', '78', '45 RPM', 'acetate disc', 'aluminum disc', 'glass disc',
        'flexi disc', 'cardboard disc', 'phonograph cylinder', 'wire recording',
        'dictabelt', 'other')
    housing_options = ('Open reel', 'Compact Audio Cassette', 'R-DAT', 'Minicassette',
        'Tape Cartridge', 'VHS', 'Other')
    reel_sizes = ('3', '5', '7', '10', '12', '14') # also Other -> empty field
    reel_size_options = [(size, '%s"' % size) for size in reel_sizes]
    reel_size_options.append((None, 'Other'))
    sound_characteristic_options = ('mono', 'stereo')
    speed_options = (
        # delimited format is aspect, value, unit
        ('tape', (
            ('tape|15/16|inches/sec', '15/16 ips'),
            ('tape|1 7/8|inches/sec', '1 7/8 ips'),
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
        ('cylinder disc', (
            ('cylinder disc|90|rpm', '90 rpm'),
            ('cylinder disc|120|rpm', '120 rpm'),
            ('cylinder disc|160|rpm', '160 rpm'),
            ('cylinder disc|other|other', 'Other'),
            ),
        ),
        ('other', (
            ('other|other|other', 'Other'),
            ),
        ),
        ('na|Not applicable|na', 'Not Applicable'),
    )
    # NOTE: speed should be displayed as ips but saved to xml as inches/sec
    # speed options is formatted for grouped options in django select widget

    # planned schema location (schema not yet available)
    #XSD_SCHEMA = 'http://pid.emory.edu/ns/2010/sourcetech/v1/sourcetech-1.xsd'
    #xmlschema = xmlmap.loadSchema(XSD_SCHEMA)
    note = xmlmap.StringField('st:note[@type="general"]', required=False,
        verbose_name='General Note', help_text='General note about the physical item')
    note_list = xmlmap.StringListField('st:note[@type="general"]')
    related_files = xmlmap.StringField('st:note[@type="relatedFiles"]', required=False,
        help_text='IDs of other digitized files for the same item, separated by semicolons. Required for multi-part items.')
        # NOTE: according to spec, related_files is required if multi-part--
        # - not tracking multi-part for Min Items (that I know of)
    conservation_history = xmlmap.StringField('st:note[@type="conservationHistory"]',
        required=False)
    conservation_history_list = xmlmap.StringListField('st:note[@type="conservationHistory"]')
    manufacturer = xmlmap.StringField('st:manufacturer', required=False,
        verbose_name='Tape Manufacturer', help_text='The manufacturer of the magnetic tape')
    speed = xmlmap.NodeField('st:speed/st:measure[@type="speed"]',
        SourceTechMeasure, instantiate_on_get=True, required=True)
    sublocation = xmlmap.StringField('st:sublocation', required=True,
        help_text='Storage location within the collection (e.g., box and folder)')
    form = xmlmap.StringField('st:form[@type="sound"]', choices=form_options,
        required=False, help_text='The physical form or medium of the resource')
    sound_characteristics = xmlmap.StringField('st:soundChar',
        choices=sound_characteristic_options, required=False)
    stock = xmlmap.StringField('st:stock', verbose_name='Tape Brand/Stock',
       help_text='The brand or stock of the magnetic tape', required=False)
    housing = xmlmap.StringField('st:housing[@type="sound"]', choices=housing_options,
        required=True, help_text='Type of housing for magnetic tape')
    reel_size =  xmlmap.NodeField('st:reelSize/st:measure[@type="width"][@aspect="reel size"]',
            SourceTechMeasure, instantiate_on_get=True, required=False)
    # tech_note is migrate/view only
    technical_note = xmlmap.StringListField('st:note[@type="technical"]', required=False)

    

class _BaseDigitalTech(xmlmap.XmlObject):
    'Base class for Digital Technical Metadata objects'
    ROOT_NS = 'http://pid.emory.edu/ns/2010/digitaltech'
    ROOT_NAMESPACES = {'dt': ROOT_NS }

class TransferEngineer(_BaseDigitalTech):
    ROOT_NAME = 'transferEngineer'
    id = xmlmap.StringField('@id')
    id_type = xmlmap.StringField('@idType')
    name = xmlmap.StringField('.')

class CodecCreator(_BaseDigitalTech):
    ROOT_NAME = 'codecCreator'
    configurations = {
        # current format is     id :  hardware, software, software version
        '1': ('Mac G4', 'DigiDesign ProTools LE',  '5.2'),
        '2': ('Mac G5', 'DigiDesign ProTools LE',  '6.7'),
        '3': ('Dell Optiplex 755', 'Apogee Rosetta',  '200'),
        '4': ('Dell Optiplex 755', 'Sound Forge',  '9.0'),
        '5': ('Dell Optiplex 755', 'iTunes',  None),
        '6': ('Unknown', 'Unknown',  None),
    }
    options = [(id, '%s - %s %s' % (c[0], c[1], c[2] if c[2] is not None else ''))
                    for id, c in configurations.iteritems()]

    id = xmlmap.StringField('dt:codecCreatorID')
    hardware = xmlmap.StringField('dt:hardware')
    software = xmlmap.StringField('dt:software')
    software_version = xmlmap.StringField('dt:softwareVersion')

class DigitalTech(_BaseDigitalTech):
    "Digital Technical Metadata."
    ROOT_NAME = 'digitaltech'
    date_captured = xmlmap.StringField('dt:dateCaptured[@encoding="w3cdtf"]',
        help_text='Date digital capture was made', required=True)
    codec_quality = xmlmap.StringField('dt:codecQuality', required=True,
        help_text='Whether the data compression method was lossless or lossy')
    duration = xmlmap.IntegerField('dt:duration/dt:measure[@type="time"][@unit="seconds"][@aspect="duration of playing time"]',
        help_text='Duration of audio playing time', required=True)
    # FIXME/TODO: note and digitization purpose could be plural
    note = xmlmap.StringField('dt:note[@type="general"]', required=False,
        help_text='Additional information that may be helpful in describing the surrogate')
    note_list = xmlmap.StringListField('dt:note[@type="general"]')
    digitization_purpose = xmlmap.StringField('dt:note[@type="purpose of digitization"]',
        required=True,
        help_text='The reason why the digital surrogate was created (e.g., exhibit, patron request, preservation)')
    digitization_purpose_list = xmlmap.StringListField('dt:note[@type="purpose of digitization"]')
    transfer_engineer = xmlmap.NodeField('dt:transferEngineer', TransferEngineer,
        instantiate_on_get=True, required=True,
        help_text='The person who performed the digitization or conversion that produced the file')
    codec_creator = xmlmap.NodeField('dt:codecCreator', CodecCreator,
        instantiate_on_get=True, required=True, # required is "Y?" in spec
        help_text='Hardware, software, and software version used to create the digital file')
    

class AudioObject(DigitalObject):
    AUDIO_CONTENT_MODEL = 'info:fedora/emory-control:EuterpeAudio-1.0'
    CONTENT_MODELS = [ AUDIO_CONTENT_MODEL ]

    mods = XmlDatastream("MODS", "MODS Metadata", AudioMods, defaults={
            'control_group': 'M',
            'format': mods.MODS_NAMESPACE,
            'versionable': True,
        })
    audio = FileDatastream("AUDIO", "Audio datastream", defaults={
            'mimetype': 'audio/x-wav',
            'versionable': True,
        })
    digtech = XmlDatastream("DigitalTech", "Technical Metadata - Digital", DigitalTech,
        defaults={
            'control_group': 'M',
            'versionable': True,
        })
    sourcetech = XmlDatastream("SourceTech", "Technical Metadata - Source", SourceTech,
        defaults={
            'control_group': 'M',
            'versionable': True,
        })

    _collection_uri = None

    def save(self, logMessage=None):
        if self.mods.isModified() or self.rels_ext.isModified or \
            self.digtech.isModified():
            # DC is derivative metadata based on MODS/RELS-EXT/Digital Tech
            # if any of them have changed, update DC
            self._update_dc()

        # for now, keep object label in sync with MODS title
        if self.mods.isModified() and self.mods.content.title:
            self.label = self.mods.content.title

        return super(AudioObject, self).save(logMessage)

    def _update_dc(self):
        '''Update Dublin Core (derivative metadata) based on master metadata
        from MODS, RELS-EXT, and digital tech metadata in order to keep data
        synchronized and make fields that need to be searchable accessible to
        Fedora findObjects API method.
         '''
        if self.mods.content.title:
            self.label = self.mods.content.title
            self.dc.content.title = self.mods.content.title
        if self.mods.content.resource_type:
            self.dc.content.type = self.mods.content.resource_type

        # clear out any dates previously in DC
        del(self.dc.content.date_list)
        if len(self.mods.content.origin_info.created) and \
                self.mods.content.origin_info.created[0].date:
            # UGH: this will add originInfo and dateCreated if they aren't already in the xml
            # because of our instantiate-on-get hack
            # FIXME: creating origin_info without at least one field may result in invalid MODS
            self.dc.content.date_list.append(self.mods.content.origin_info.created[0].date)
        if len(self.mods.content.origin_info.issued) and \
                self.mods.content.origin_info.issued[0].date:
            # ditto on UGH/FIXME for date created
            self.dc.content.date_list.append(self.mods.content.origin_info.issued[0].date)

        # FIXME: detect if origin info is empty & remove it so we don't get invalid MODS

        # clear out any descriptions previously in DC and set from MODS/DigTech
        del(self.dc.content.description_list)
        if self.mods.content.general_note.text:
            self.dc.content.description_list.append(self.mods.content.general_note.text)
        # digitization_purpose
        if self.digtech.content.digitization_purpose:
            self.dc.content.description_list.extend(self.digtech.content.digitization_purpose_list)
        # Currently not indexing general note in digital tech

        # clear out any rights previously in DC and set contents from MODS accessCondition
        del(self.dc.content.rights_list)
        if self.mods.content.access_conditions:
            # use access condition type as a label
            for access in self.mods.content.access_conditions:
                self.dc.content.rights_list.append('%s: %s' % \
                    (access.type, access.text))

        # TEMPORARY: collection relation and cmodel must be in DC for find_objects
        # - these can be removed once we implement gsearch
        if self.collection_uri is not None:
            # store collection membership as dc:relation
            self.dc.content.relation = str(self.collection_uri)
        # set collection content model URI as dc:format
        self.dc.content.format = self.AUDIO_CONTENT_MODEL

    @staticmethod
    def init_from_file(filename, initial_label=None, request=None, checksum=None):
        '''Static method to create a new :class:`AudioObject` instance from
        a file.  Sets the object label and metadata title based on the initial
        label specified, or file basename.  Also sets the following default
        metadata values:
            * mods:typeOfResource = "sound recording"

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
        # set initial mods:typeOfResource - all AudioObjects default to sound recording
        obj.mods.content.resource_type = 'sound recording'
        # set codec quality to lossless in digital tech metadata 
        # - default for AudioObjects, should only accept lossless audio for master file
        obj.digtech.content.codec_quality = 'lossless'
        # get wav duration and store in digital tech metadata
        obj.digtech.content.duration = '%d' % round(wav_duration(filename))

        return obj

    def _get_collection_uri(self):
        # for now, an audio object should only have one isMemberOfCollection relation
        if self._collection_uri is None:
            self._collection_uri = self.rels_ext.content.value(
                        subject=self.uriref,
                        predicate=relsext.isMemberOfCollection)
        return self._collection_uri

    def _set_collection_uri(self, collection_uri):
        if not isinstance(collection_uri, URIRef):
            collection_uri = URIRef(collection_uri)

        # update/replace any existing collection membership (only one allowed, for now)
        self.rels_ext.content.set((
            self.uriref,
            relsext.isMemberOfCollection,
            collection_uri))
        # clear out any cached collection id
        self._collection_uri = None

    collection_uri = property(_get_collection_uri, _set_collection_uri)


def wav_duration(filename):
    '''Calculate the duration of a WAV file using Python's built in :mod:`wave`
    library.  Raises a StandardError if file cannot be read as a WAV.

    :param filename: full path to the WAV file
    :returns: duration in seconds as a float
    '''
    try:
        wav_file = wave.open(filename, 'rb')
    except wave.Error as werr:
        # FIXME: is there a better/more specific exception that can be used here?
        raise StandardError('Failed to open file %s as a WAV due to: %s' % (filename, werr))
    # any other file errors will be propagated as IOError
    
    # duration in secdons = number of samples / sampling frequency
    duration = float(wav_file.getnframes())/float(wav_file.getframerate())
    return duration
