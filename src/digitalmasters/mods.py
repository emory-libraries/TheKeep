'''
:mod:`eulcore.xmlmap` classes for dealing with the MODS metadata format
(Metadata Object Description Schema).

'''

from eulcore import xmlmap

MODS_NAMESPACE = 'http://www.loc.gov/mods/v3'
MODS_SCHEMA = "http://www.loc.gov/standards/mods/mods.xsd"
MODSv34_SCHEMA = "http://www.loc.gov/standards/mods/v3/mods-3-4.xsd"

# MODS schema is loaded by several of the mods classes - load once and reuse
_mods_xmlschema = xmlmap.loadSchema(MODS_SCHEMA)

class Common(xmlmap.XmlObject):
    "MODS class with namespace declaration common to all MODS XmlObjects."
    ROOT_NS = MODS_NAMESPACE
    ROOT_NAMESPACES = {'mods': MODS_NAMESPACE }

class Date(Common):
    '''MODS date element (common fields for the dates under mods:originInfo).'''
    # this class not meant for direct use; should be extended for specific dates.
    # FIXME: schema required here for schemafields; this should be refactored
    XSD_SCHEMA = MODS_SCHEMA
    xmlschema = _mods_xmlschema
    date = xmlmap.StringField('.') 
    key_date = xmlmap.SimpleBooleanField('@keyDate', 'yes', false=None)
    encoding = xmlmap.SchemaField('@encoding', 'dateEncodingAttributeDefinition')
    point = xmlmap.SchemaField('@point', 'datePointAttributeDefinition')
    qualifier = xmlmap.SchemaField('@qualifier', 'dateQualifierAttributeDefinition')

class DateCreated(Date):
    ROOT_NAME = 'dateCreated'

class DateIssued(Date):
    ROOT_NAME = 'dateIssued'

class OriginInfo(Common):
    "MODS originInfo element (incomplete)"
    ROOT_NAME = 'originInfo'
    created = xmlmap.NodeListField('mods:dateCreated', DateCreated,
        verbose_name='Date Created',
        help_text='Date the resource was first created (e.g., date of recording,' +
            ' photograph taken, or letter written)')
    issued = xmlmap.NodeListField('mods:dateIssued', DateIssued,
        verbose_name='Date Created',
        help_text='Date the resource was published, released, or issued')

class Note(Common):
    "MODS note element"
    ROOT_NAME = 'note'
    label = xmlmap.StringField('@displayLabel')
    type = xmlmap.StringField('@type',
                choices=['general', 'inscription', 'source of information',
                        'reference', 'hidden'])
        # with capacity to add to the list ?
    text = xmlmap.StringField('.')      # actual text value of the note

class Identifier(Common):
    'MODS identifier'
    ROOT_NAME = 'identifier'
    type = xmlmap.StringField('@type')
    text = xmlmap.StringField('.')

class AccessCondition(Common):
    "MODS accessCondition"
    ROOT_NAME = 'accessCondition'
    type = xmlmap.StringField('@type',
            choices=['restrictions on access', 'use and reproduction'])
    text = xmlmap.StringField('.')

class NamePart(Common):
    "MODS namePart"
    ROOT_NAME = 'namePart'
    # FIXME: schema required here for schemafields; this should be refactored
    XSD_SCHEMA = MODS_SCHEMA
    xmlschema = _mods_xmlschema

    type = xmlmap.SchemaField('@type', 'namePartTypeAttributeDefinition',
                              required=False) # type is optional
    text = xmlmap.StringField('.')

class Role(Common):
    "MODS role"
    ROOT_NAME = 'role'
    type = xmlmap.StringField('mods:roleTerm/@type')
    authority = xmlmap.StringField('mods:roleTerm/@authority', choices=['', 'marcrelator', 'local'])
    text = xmlmap.StringField('mods:roleTerm')

class Name(Common):
    "MODS name"
    ROOT_NAME = 'name'
    # FIXME: schema required here for schemafields; this should be refactored
    XSD_SCHEMA = MODS_SCHEMA
    xmlschema = _mods_xmlschema

    type = xmlmap.SchemaField('@type', 'nameTypeAttributeDefinition')
    authority = xmlmap.StringField('@authority', choices=['local', 'naf']) # naf = NACO authority file
    id = xmlmap.StringField('@ID')  # optional
    name_parts = xmlmap.NodeListField('mods:namePart', NamePart)
    display_form = xmlmap.StringField('mods:displayForm')
    affiliation = xmlmap.StringField('mods:affiliation')
    roles = xmlmap.NodeListField('mods:role', Role)

    def __unicode__(self):
        # default text display of a name (excluding roles for now)
        # TODO: improve logic for converting to plain-text name
        # (e.g., for template display, setting as dc:creator, etc)
        return ' '.join([unicode(part) for part in self.name_parts])

class BaseMods(Common):
    """Common field declarations for all top-level MODS elements; base class for
    :class:`MODS` and :class:`RelatedItem`."""
    XSD_SCHEMA = MODS_SCHEMA
    xmlschema = _mods_xmlschema

    title = xmlmap.StringField("mods:titleInfo/mods:title")
    resource_type  = xmlmap.SchemaField("mods:typeOfResource", "resourceTypeDefinition")
    name = xmlmap.NodeField('mods:name', Name, instantiate_on_get=True)  # single name for now
    note = xmlmap.NodeField('mods:note', Note, instantiate_on_get=True)
    origin_info = xmlmap.NodeField('mods:originInfo', OriginInfo, instantiate_on_get=True)
    record_id = xmlmap.StringField('mods:recordInfo/mods:recordIdentifier')
    identifiers = xmlmap.NodeListField('mods:identifier', Identifier)
    access_conditions = xmlmap.NodeListField('mods:accessCondition', AccessCondition)

class RelatedItem(BaseMods):
    "MODS relatedItem: contains all the top-level MODS fields, plus a type attribute."
    ROOT_NAME = 'relatedItem'
    # FIXME: schema required here for schemafields; this should be refactored
    XSD_SCHEMA = MODS_SCHEMA
    xmlschema = _mods_xmlschema
    type = xmlmap.SchemaField("@type", 'relatedItemTypeAttributeDefinition')

class MODS(BaseMods):
    '''Top-level XmlObject for a MODS metadata record.  Inherits all standard top-level
    MODS fields from :class:`BaseMods` and adds a mapping for :class:`RelatedItem`.
    '''
    ROOT_NAME = 'mods'
    XSD_SCHEMA = MODS_SCHEMA
    xmlschema = _mods_xmlschema
    related_items = xmlmap.NodeListField('mods:relatedItem', RelatedItem)


class MODSv34(MODS):
    '''MODS version 3.4.  Currently consists of all the same fields as
    :class:`MODS`, but loads the MODS version 3.4 schema for validation.
    '''
    XSD_SCHEMA = MODSv34_SCHEMA
    xmlschema = xmlmap.loadSchema(XSD_SCHEMA)
    # FIXME: how to set version attribute when creating from scratch?
