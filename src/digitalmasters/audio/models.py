import os
from rdflib import URIRef
import wave

from eulcore import xmlmap
from eulcore.fedora.models import FileDatastream, XmlDatastream, URI_HAS_MODEL

from digitalmasters.fedora import DigitalObject, Repository
from digitalmasters import mods

class DigitalTech(xmlmap.XmlObject):
    # ROUGH version of xmlmap for digital technical metadata - incomplete
    "Digital Technical Metadata."
    ROOT_NS = 'http://pid.emory.edu/ns/2010/digital-tech-metadata' 
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

    mods = XmlDatastream("MODS", "MODS Metadata", mods.MODS, defaults={
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

    def save(self, logMessage=None):
        if self.mods.isModified():
            # MODS is master metadata
            # if it has changed, update DC and object label to keep them in sync
            if self.mods.content.title:
                self.label = self.mods.content.title
                self.dc.content.title = self.mods.content.title
            if self.mods.content.resource_type:
                self.dc.content.type = self.mods.content.resource_type
            if len(self.mods.content.origin_info.created) and \
                self.mods.content.origin_info.created[0].date:
                # UGH: this will add originInfo and dateCreated if they aren't already in the xml
                # because of our instantiate-on-get hack
                # FIXME: creating origin_info without at least one field may result in invalid MODS
                self.dc.content.date = self.mods.content.origin_info.created[0].date
                
        return super(AudioObject, self).save(logMessage)

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