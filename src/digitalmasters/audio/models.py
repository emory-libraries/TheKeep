import os
from rdflib import URIRef
import wave

from eulcore import xmlmap
from eulcore.fedora.models import FileDatastream, XmlDatastream, URI_HAS_MODEL
from eulcore.fedora.rdfns import relsext

from digitalmasters.fedora import DigitalObject, Repository
from digitalmasters import mods


class AudioMods(mods.MODS):
    """AudioObject-specific MODS, based on :class:`mods.MODS`."""
    # possibly map identifier type uri as well ?
    general_note = xmlmap.NodeField('mods:note[@type="general"]',
                                          mods.Note, instantiate_on_get=True)
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
        ('tape', (
            ('15/16 inches/sec', '15/16 ips'),
            ('1 7/8 inches/sec', '1 7/8 ips'),
            ('3 3/4 inches/sec', '3 3/4 ips'),
            ('7 1/2 inches/sec', '7 1/2 ips'),
            ('15 inches/sec', '15 ips'),
            ('30 inches/sec', '30 ips'),
            )
         ), # Other ?
        ('phono disc', (
            ('16 rpm', '16 rpm'),
            ('33 1/3 rpm', '33 1/3 rpm'),
            ('45 rpm', '45 rpm'),
            ('78 rpm', '78 rpm'),
            )
        ), # other ?
        ('cylinder disc', (
            ('90 rpm', '90 rpm'),
            ('120 rpm', '120 rpm'),
            ('160 rpm', '160 rpm'), # other?
            )
        )
    )
    # NOTE: speed should be displayed as ips but saved to xml as inches/sec
    # speed options is formatted for grouped options in django select widget

    # planned schema location (schema not yet available)
    #XSD_SCHEMA = 'http://pid.emory.edu/ns/2010/sourcetech/v1/sourcetech-1.xsd'
    #xmlschema = xmlmap.loadSchema(XSD_SCHEMA)
    note = xmlmap.StringField('st:note[@type="general"]')
    note_list = xmlmap.StringListField('st:note[@type="general"]')
    related_files = xmlmap.StringField('st:note[@type="relatedFiles"]')
    conservation_history = xmlmap.StringField('st:note[@type="conservationHistory"]')
    conservation_history_list = xmlmap.StringListField('st:note[@type="conservationHistory"]')
    manufacturer = xmlmap.StringField('st:manufacturer')
    speed = xmlmap.NodeField('st:speed/st:measure[@type="speed"]',
            SourceTechMeasure, instantiate_on_get=True)
    sublocation = xmlmap.StringField('st:sublocation')
    form = xmlmap.StringField('st:form[@type="sound"]', choices=form_options)
    sound_characteristics = xmlmap.StringField('st:soundChar', choices=sound_characteristic_options)
    stock = xmlmap.StringField('st:stock')
    housing = xmlmap.StringField('st:housing[@type="sound"]', choices=housing_options)
    reel_size =  xmlmap.NodeField('st:reelSize/st:measure[@type="width"][@aspect="reel size"]',
            SourceTechMeasure, instantiate_on_get=True)
    # tech_note is migrate/view only
    technical_note = xmlmap.StringListField('st:note[@type="technical"]')

    


class DigitalTech(xmlmap.XmlObject):
    # ROUGH version of xmlmap for digital technical metadata - incomplete
    "Digital Technical Metadata."
    ROOT_NS = 'http://pid.emory.edu/ns/2010/digitaltech' 
    ROOT_NAMESPACES = {'dt': ROOT_NS }
    ROOT_NAME = 'dt'    # tentative/temporary
    date_captured = xmlmap.StringField('dt:dateCaptured[@encoding="w3cdft"]')
    codec_quality = xmlmap.StringField('dt:codecQuality')
    duration = xmlmap.IntegerField('dt:duration/dt:measure[@type="time"][@unit="seconds"][@aspect="duration of playing time"]')
    note = xmlmap.StringListField('dt:note[@type="general"]')
    digitization_purpose = xmlmap.StringListField('dt:note[@type="purpose of digitization"]')
    transfer_engineer = xmlmap.StringField('transferEngineerID')
    # TODO: split out transfer engineer into sub object with attributes
    # TODO: codec creator
    

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
            self.dc.content.description_list.extend(self.digtech.content.digitization_purpose)
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
