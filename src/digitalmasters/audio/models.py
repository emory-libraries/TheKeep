from eulcore import xmlmap
from eulcore.fedora.models import DigitalObject, FileDatastream, RdfDatastream, XmlDatastream
from eulcore.xmlmap.dc import DublinCore

class ModsBase(xmlmap.XmlObject):
    "Base MODS class with namespace declaration to be shared by all MODS XmlObjects."
    ROOT_NS = 'http://www.loc.gov/mods/v3'
    ROOT_NAMESPACES = {'mods': ROOT_NS }

class ModsDate(ModsBase):
    "MODS date element (common fields for the dates under mods:originInfo)"
    ROOT_NAME = 'dateCreated'       # ?? could vary
    date = xmlmap.StringField('.')     # date field?
    key_date = xmlmap.SimpleBooleanField('@keyDate', 'yes', false=None)
    encoding = xmlmap.StringField('@encoding')
    point = xmlmap.StringField('@point')
    qualifier = xmlmap.StringField('@qualifier')

class ModsOriginInfo(ModsBase):
    "MODS originInfo element (incomplete)"
    ROOT_NAME = 'originInfo'
    created = xmlmap.NodeField('mods:dateCreated', ModsDate, instantiate_on_get=True)

class ModsNote(ModsBase):
    "MODS note element"
    ROOT_NAME = 'note'
    label = xmlmap.StringField('@displayLabel')
    type = xmlmap.StringField('@type',
                choices=['general', 'inscription', 'source of information', 
                        'reference', 'hidden'])
        # with capacity to add to the list ?
    text = xmlmap.StringField('.')      # actual text value of the note

class Mods(ModsBase):
    """
    Prototype XmlObject for MODS metadata.

    Only a limited field set for now.
    """

    ROOT_NAME = 'mods'

    XSD_SCHEMA = "http://www.loc.gov/standards/mods/mods.xsd"
    xmlschema = xmlmap.loadSchema(XSD_SCHEMA)
    
    title = xmlmap.StringField("mods:titleInfo/mods:title")
    resource_type  = xmlmap.SchemaField("mods:typeOfResource", "resourceTypeDefinition")
    note = xmlmap.NodeField('mods:note', ModsNote, instantiate_on_get=True)
    origin_info = xmlmap.NodeField('mods:originInfo', ModsOriginInfo, instantiate_on_get=True)
    record_id = xmlmap.StringField('mods:recordInfo/mods:recordIdentifier')


class CollectionObject(DigitalObject):
    CONTENT_MODELS = [ 'emory-control:Collection-1.1' ]

    mods = XmlDatastream('MODS', 'MODS Metadata', Mods, defaults={
            'control_group': 'M',
            'format': Mods.ROOT_NS,
            'versionable': True,
        })

class AudioObject(DigitalObject):
    CONTENT_MODELS = [ 'emory-control:EuterpeAudio-1.0' ]

    mods = XmlDatastream("MODS", "MODS Metadata", Mods, defaults={
            'control_group': 'M',
            'format': Mods.ROOT_NS,
            'versionable': True,
        })
    audio = FileDatastream("AUDIO", "Audio datastream", defaults={
            'mimetype': 'audio/x-wav',
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
            if self.mods.content.origin_info.created.date:
                # UGH: this will add originInfo and dateCreated if they aren't already in the xml
                # because of our instantiate-on-get hack
                self.dc.content.date = self.mods.content.origin_info.created.date
                
        return super(AudioObject, self).save(logMessage)
