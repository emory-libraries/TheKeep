'''
:mod:`eulcore.xmlmap` classes for dealing with the MODS metadata format
(Metadata Object Description Schema).

'''

from eulcore import xmlmap

MODS_NAMESPACE = 'http://www.loc.gov/mods/v3'
MODS_SCHEMA = "http://www.loc.gov/standards/mods/mods.xsd"
MODSv34_SCHEMA = "http://www.loc.gov/standards/mods/v3/mods-3-4.xsd"

class ModsCommon(xmlmap.XmlObject):
    "MODS class with namespace declaration common to all MODS XmlObjects."
    ROOT_NS = MODS_NAMESPACE
    ROOT_NAMESPACES = {'mods': MODS_NAMESPACE }

class ModsDate(ModsCommon):
    "MODS date element (common fields for the dates under mods:originInfo)"
    ROOT_NAME = 'dateCreated'       # ?? could vary
    # FIXME: schema required here for schemafields; this should be refactored
    XSD_SCHEMA = MODS_SCHEMA
    xmlschema = xmlmap.loadSchema(XSD_SCHEMA)
    date = xmlmap.StringField('.')     # date field?
    key_date = xmlmap.SimpleBooleanField('@keyDate', 'yes', false=None)
    encoding = xmlmap.SchemaField('@encoding', 'dateEncodingAttributeDefinition')
    point = xmlmap.SchemaField('@point', 'datePointAttributeDefinition')
    qualifier = xmlmap.SchemaField('@qualifier', 'dateQualifierAttributeDefinition')

class ModsOriginInfo(ModsCommon):
    "MODS originInfo element (incomplete)"
    ROOT_NAME = 'originInfo'
    created = xmlmap.NodeListField('mods:dateCreated', ModsDate)

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
    XSD_SCHEMA = MODS_SCHEMA
    xmlschema = xmlmap.loadSchema(XSD_SCHEMA)

    type = xmlmap.SchemaField('@type', 'namePartTypeAttributeDefinition',
                              required=False) # type is optional
    text = xmlmap.StringField('.')

class ModsRole(ModsCommon):
    "MODS role"
    ROOT_NAME = 'role'
    type = xmlmap.StringField('mods:roleTerm/@type')
    authority = xmlmap.StringField('mods:roleTerm/@authority', choices=['', 'marcrelator', 'local'])
    text = xmlmap.StringField('mods:roleTerm')

class ModsName(ModsCommon):
    "MODS name"
    ROOT_NAME = 'name'
    # FIXME: schema required here for schemafields; this should be refactored
    XSD_SCHEMA = MODS_SCHEMA
    xmlschema = xmlmap.loadSchema(XSD_SCHEMA)

    type = xmlmap.SchemaField('@type', 'nameTypeAttributeDefinition')
    authority = xmlmap.StringField('@authority', choices=['local', 'naf']) # naf = NACO authority file
    id = xmlmap.StringField('@ID')  # optional
    name_parts = xmlmap.NodeListField('mods:namePart', ModsNamePart)
    display_form = xmlmap.StringField('mods:displayForm')
    affiliation = xmlmap.StringField('mods:affiliation')
    roles = xmlmap.NodeListField('mods:role', ModsRole)

    def __unicode__(self):
        # default text display of a name (excluding roles for now)
        # TODO: improve logic for converting to plain-text name
        # (e.g., for template display, setting as dc:creator, etc)
        return ' '.join([unicode(part) for part in self.name_parts])

class ModsBase(ModsCommon):
    """Common field declarations for all top-level MODS elements; base class for
    :class:`Mods` and :class:`ModsRelatedItem`."""
    XSD_SCHEMA = MODS_SCHEMA
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
    XSD_SCHEMA = MODS_SCHEMA
    xmlschema = xmlmap.loadSchema(XSD_SCHEMA)
    type = xmlmap.SchemaField("@type", 'relatedItemTypeAttributeDefinition')

class Mods(ModsBase):
    """
    Prototype XmlObject for MODS metadata.

    Only a limited field set for now.
    """
    ROOT_NAME = 'mods'
    XSD_SCHEMA = MODS_SCHEMA
    xmlschema = xmlmap.loadSchema(XSD_SCHEMA)
    related_items = xmlmap.NodeListField('mods:relatedItem', ModsRelatedItem)


class Modsv34(Mods):
    XSD_SCHEMA = MODSv34_SCHEMA
    xmlschema = xmlmap.loadSchema(XSD_SCHEMA)
    # FIXME: how to set version attribute when creating from scratch?
