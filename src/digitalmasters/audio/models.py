from eulcore import xmlmap
from eulcore.fedora.models import DigitalObject, FileDatastream, RdfDatastream, XmlDatastream
from eulcore.xmlmap.dc import DublinCore

class AudioObject(DigitalObject):
    dc = XmlDatastream("DC", "Dublin Core", DublinCore, defaults={
            'control_group': 'X',
            'format': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
        })
    rels_ext = RdfDatastream("RELS-EXT", "External Relations", defaults={
            'control_group': 'X',
            'format': 'info:fedora/fedora-system:FedoraRELSExt-1.0',
        })
    audio = FileDatastream("AUDIO", "Audio datastream", defaults={
            'mimetype': 'audio/x-wav',
        })

class ModsDate(xmlmap.XmlObject):
    ROOT_NAME = 'dateCreated'       # ?? could vary
    key_date = xmlmap.SimpleBooleanField('@keyDate', 'yes', '')    # FIXME: not really a simple boolean...
    date = xmlmap.StringField('.')     # date field?

class ModsOriginInfo(xmlmap.XmlObject):
    ROOT_NAME = 'originInfo'
    created = xmlmap.NodeField('mods:dateCreated', ModsDate)

class ModsNote(xmlmap.XmlObject):
    ROOT_NAME = 'note'
    label = xmlmap.StringField('@displayLabel')
    type = xmlmap.StringField('@type',
                choices=['general', 'inscription', 'source of information', 
                        'reference', 'hidden'])
        # with capacity to add to the list ?
    text = xmlmap.StringField('.')      # actual text value of the note

class Mods(xmlmap.XmlObject):
    """
    Prototype XmlObject for MODS metadata.

    Only a limited field set for now.
    """

    ROOT_NS = 'http://www.loc.gov/mods/v3'
    ROOT_NAME = 'mods'
    ROOT_NAMESPACES = {'mods': ROOT_NS }

    XSD_SCHEMA = "http://www.loc.gov/standards/mods/mods.xsd"
    xmlschema = xmlmap.loadSchema(XSD_SCHEMA)
    
    title = xmlmap.StringField("mods:titleInfo/mods:title")
    resource_type  = xmlmap.SchemaField("mods:typeOfResource", "resourceTypeDefinition")
    note = xmlmap.NodeField('mods:note', ModsNote)
    origin_info = xmlmap.NodeField('mods:originInfo', ModsOriginInfo)

