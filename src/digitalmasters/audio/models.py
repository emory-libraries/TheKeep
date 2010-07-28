from eulcore import xmlmap
from eulcore.fedora.models import DigitalObject, FileDatastream, XmlDatastream

class ModsCommon(xmlmap.XmlObject):
    "MODS class with namespace declaration common to all MODS XmlObjects."
    ROOT_NS = 'http://www.loc.gov/mods/v3'
    ROOT_NAMESPACES = {'mods': ROOT_NS }
    
class ModsDate(ModsCommon):
    "MODS date element (common fields for the dates under mods:originInfo)"
    ROOT_NAME = 'dateCreated'       # ?? could vary
    # FIXME: schema required here for schemafields; this should be refactored
    XSD_SCHEMA = "http://www.loc.gov/standards/mods/mods.xsd"
    xmlschema = xmlmap.loadSchema(XSD_SCHEMA)
    date = xmlmap.StringField('.')     # date field?
    key_date = xmlmap.SimpleBooleanField('@keyDate', 'yes', false=None)
    encoding = xmlmap.SchemaField('@encoding', 'dateEncodingAttributeDefinition')
    point = xmlmap.SchemaField('@point', 'datePointAttributeDefinition')
    qualifier = xmlmap.SchemaField('@qualifier', 'dateQualifierAttributeDefinition')

class ModsOriginInfo(ModsCommon):
    "MODS originInfo element (incomplete)"
    ROOT_NAME = 'originInfo'
    created = xmlmap.NodeField('mods:dateCreated', ModsDate, instantiate_on_get=True)

class ModsNote(ModsCommon):
    "MODS note element"
    ROOT_NAME = 'note'
    label = xmlmap.StringField('@displayLabel')
    type = xmlmap.StringField('@type',
                choices=['general', 'inscription', 'source of information', 
                        'reference', 'hidden'])
        # with capacity to add to the list ?
    text = xmlmap.StringField('.')      # actual text value of the note

class ModsIdentifier(ModsCommon):
    'MODS identifier'
    ROOT_NAME = 'identifier'
    type = xmlmap.StringField('@type')
    text = xmlmap.StringField('.')

class ModsAccessCondition(ModsCommon):
    "MODS accessCondition"
    ROOT_NAME = 'accessCondition'
    type = xmlmap.StringField('@type',
            choices=['restrictions on access', 'use and reproduction'])
    text = xmlmap.StringField('.')

class ModsNamePart(ModsCommon):
    "MODS namePart"
    ROOT_NAME = 'namePart'
    # FIXME: schema required here for schemafields; this should be refactored
    XSD_SCHEMA = "http://www.loc.gov/standards/mods/mods.xsd"
    xmlschema = xmlmap.loadSchema(XSD_SCHEMA)

    type = xmlmap.SchemaField('@type', 'namePartTypeAttributeDefinition') # optional 
    text = xmlmap.StringField('.')

class ModsRole(ModsCommon):
    "MODS role"
    ROOT_NAME = 'role'
    type = xmlmap.StringField('mods:roleTerm/@type')
    authority = xmlmap.StringField('mods:roleTerm/@authority')
    text = xmlmap.StringField('mods:roleTerm')

class ModsName(ModsCommon):
    "MODS name"
    ROOT_NAME = 'name'
    # FIXME: schema required here for schemafields; this should be refactored
    XSD_SCHEMA = "http://www.loc.gov/standards/mods/mods.xsd"
    xmlschema = xmlmap.loadSchema(XSD_SCHEMA)

    type = xmlmap.SchemaField('@type', 'nameTypeAttributeDefinition')
    authority = xmlmap.StringField('@authority')    # choices local/naf - form detail?
    id = xmlmap.StringField('@ID')  # optional
    name_parts = xmlmap.NodeListField('mods:namePart', ModsNamePart)
    display_form = xmlmap.StringField('mods:displayForm')
    affiliation = xmlmap.StringField('mods:affiliation')
    roles = xmlmap.NodeListField('mods:role', ModsRole)

class ModsBase(ModsCommon):
    """Common field declarations for all top-level MODS elements; base class for
    :class:`Mods` and :class:`ModsRelatedItem`."""
    XSD_SCHEMA = "http://www.loc.gov/standards/mods/mods.xsd"
    xmlschema = xmlmap.loadSchema(XSD_SCHEMA)
    
    title = xmlmap.StringField("mods:titleInfo/mods:title")
    resource_type  = xmlmap.SchemaField("mods:typeOfResource", "resourceTypeDefinition")
    name = xmlmap.NodeField('mods:name', ModsName, instantiate_on_get=True)  # single name for now
    note = xmlmap.NodeField('mods:note', ModsNote, instantiate_on_get=True)
    origin_info = xmlmap.NodeField('mods:originInfo', ModsOriginInfo, instantiate_on_get=True)
    record_id = xmlmap.StringField('mods:recordInfo/mods:recordIdentifier')
    identifiers = xmlmap.NodeListField('mods:identifier', ModsIdentifier)
    access_conditions = xmlmap.NodeListField('mods:accessCondition', ModsAccessCondition)

class ModsRelatedItem(ModsBase):
    "MODS relatedItem: contains all the top-level MODS fields, plus a type attribute."
    ROOT_NAME = 'relatedItem'
    # FIXME: schema required here for schemafields; this should be refactored
    XSD_SCHEMA = "http://www.loc.gov/standards/mods/mods.xsd"
    xmlschema = xmlmap.loadSchema(XSD_SCHEMA)
    type = xmlmap.SchemaField("@type", 'relatedItemTypeAttributeDefinition')

class Mods(ModsBase):
    """
    Prototype XmlObject for MODS metadata.

    Only a limited field set for now.
    """
    ROOT_NAME = 'mods'
    XSD_SCHEMA = "http://www.loc.gov/standards/mods/mods.xsd"
    xmlschema = xmlmap.loadSchema(XSD_SCHEMA)
    related_items = xmlmap.NodeListField('mods:relatedItem', ModsRelatedItem)
    
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
