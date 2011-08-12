'''
:mod:`eulxml.xmlmap` classes for dealing with the
`MODS <http://www.loc.gov/standards/mods/>`_ metadata format
(Metadata Object Description Schema).
'''

from eulxml import xmlmap

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
    ''':class:`~eulxml.xmlmap.XmlObject` for MODS date element (common fields
    for the dates under mods:originInfo).'''
    # this class not meant for direct use; should be extended for specific dates.
    # FIXME: schema required here for schemafields; this should be refactored
    XSD_SCHEMA = MODS_SCHEMA
    xmlschema = _mods_xmlschema
    date = xmlmap.StringField('text()')
    key_date = xmlmap.SimpleBooleanField('@keyDate', 'yes', false=None)
    encoding = xmlmap.SchemaField('@encoding', 'dateEncodingAttributeDefinition')
    point = xmlmap.SchemaField('@point', 'datePointAttributeDefinition')
    qualifier = xmlmap.SchemaField('@qualifier', 'dateQualifierAttributeDefinition')

    def is_empty(self):
        '''Returns False if no date value is set; returns True if any date value
        is set.  Attributes are ignored for determining whether or not the
        date should be considered empty, as they are only meaningful in
        reference to a date value.'''
        return not self.node.text

class DateCreated(Date):
    ROOT_NAME = 'dateCreated'

class DateIssued(Date):
    ROOT_NAME = 'dateIssued'

class OriginInfo(Common):
    ":class:`~eulxml.xmlmap.XmlObject` for MODS originInfo element (incomplete)"
    ROOT_NAME = 'originInfo'
    created = xmlmap.NodeListField('mods:dateCreated', DateCreated,
        verbose_name='Date Created',
        help_text='Date the resource was first created (e.g., date of recording,' +
            ' photograph taken, or letter written)')
    issued = xmlmap.NodeListField('mods:dateIssued', DateIssued,
        verbose_name='Date Issued',
        help_text='Date the resource was published, released, or issued')

    def is_empty(self):
        """Returns True if all child date elements present are empty.  Returns
        False if any child date elements are not empty."""
        return all(date.is_empty() for date in set.union(set(self.created), set(self.issued)))

class RecordInfo(Common):
    ROOT_NAME = 'recordInfo'
    record_id = xmlmap.StringField('mods:recordIdentifier')
    record_origin = xmlmap.StringField('mods:recordOrigin')
    creation_date = xmlmap.StringField('mods:recordCreationDate[@encoding="w3cdtf"]')
    change_date = xmlmap.StringField('mods:recordChangeDate[@encoding="w3cdtf"]')

class Note(Common):
    ":class:`~eulxml.xmlmap.XmlObject` for MODS note element"
    ROOT_NAME = 'note'
    label = xmlmap.StringField('@displayLabel')
    type = xmlmap.StringField('@type')
#                choices=['general', 'inscription', 'source of information',
#                        'reference', 'hidden'])
        # with capacity to add to the list ?
        # FIXME: keep-specific note type choices should not be defined here
    text = xmlmap.StringField('text()')      # actual text value of the note

class TypedNote(Note):
    '''Extends :class:`Note` to modify :meth:`is_empty` behavior-- considered
    empty even when a type attribute is set.'''
    
    def is_empty(self):
        """Returns True if the root node contains no child elements, no text,
        and no attributes other than **type**. Returns False if any are present."""
        non_type_attributes = [attr for attr in self.node.attrib.keys() if attr != 'type']
        return len(self.node) == 0 and len(non_type_attributes) == 0 \
            and not self.node.text and not self.node.tail


class Identifier(Common):
    ':class:`~eulxml.xmlmap.XmlObject` for MODS identifier'
    ROOT_NAME = 'identifier'
    type = xmlmap.StringField('@type')
    text = xmlmap.StringField('text()')

class AccessCondition(Common):
    ':class:`~eulxml.xmlmap.XmlObject` for MODS accessCondition'
    ROOT_NAME = 'accessCondition'
    type = xmlmap.StringField('@type',
            choices=['restrictions on access', 'use and reproduction'])
    text = xmlmap.StringField('text()')

class NamePart(Common):
    ':class:`~eulxml.xmlmap.XmlObject` for MODS namePart'
    ROOT_NAME = 'namePart'
    # FIXME: schema required here for schemafields; this should be refactored
    XSD_SCHEMA = MODS_SCHEMA
    xmlschema = _mods_xmlschema

    type = xmlmap.SchemaField('@type', 'namePartTypeAttributeDefinition',
                              required=False) # type is optional
    text = xmlmap.StringField('text()')

class Role(Common):
    ':class:`~eulxml.xmlmap.XmlObject` for MODS role'
    ROOT_NAME = 'role'
    type = xmlmap.StringField('mods:roleTerm/@type')
    authority = xmlmap.StringField('mods:roleTerm/@authority', choices=['', 'marcrelator', 'local'])
    text = xmlmap.StringField('mods:roleTerm')

class Name(Common):
    ':class:`~eulxml.xmlmap.XmlObject` for MODSRelatedItem name'
    ROOT_NAME = 'name'
    # FIXME: schema required here for schemafields; this should be refactored
    XSD_SCHEMA = MODS_SCHEMA
    xmlschema = _mods_xmlschema

    type = xmlmap.SchemaField('@type', 'nameTypeAttributeDefinition', required=False)
    authority = xmlmap.StringField('@authority', choices=['', 'local', 'naf'], required=False) # naf = NACO authority file
    id = xmlmap.StringField('@ID', required=False)  # optional
    name_parts = xmlmap.NodeListField('mods:namePart', NamePart)
    display_form = xmlmap.StringField('mods:displayForm')
    affiliation = xmlmap.StringField('mods:affiliation')
    roles = xmlmap.NodeListField('mods:role', Role)

    def __unicode__(self):
        # default text display of a name (excluding roles for now)
        # TODO: improve logic for converting to plain-text name
        # (e.g., for template display, setting as dc:creator, etc)
        return ' '.join([unicode(part) for part in self.name_parts])

class Genre(Common):
    ROOT_NAME = 'genre'
    authority = xmlmap.StringField('@authority')
    text = xmlmap.StringField('text()')

class LanguageTerm(Common):
    ROOT_NAME = 'languageTerm'
    type = xmlmap.StringField('@type')
    authority = xmlmap.StringField('@authority')
    text = xmlmap.StringField('text()')

class Language(Common):
    ROOT_NAME = 'language'
    terms = xmlmap.NodeListField('mods:languageTerm', LanguageTerm)

class Subject(Common):
    ROOT_NAME = 'subject'
    authority = xmlmap.StringField('@authority')

    # and one of the following:
    geographic = xmlmap.StringField('mods:geographic')
    name = xmlmap.NodeField('mods:name', Name)
    topic = xmlmap.StringField('mods:topic')
    title = xmlmap.StringField('mods:titleInfo/mods:title')

class BaseMods(Common):
    ''':class:`~eulxml.xmlmap.XmlObject` with common field declarations for all
    top-level MODS elements; base class for :class:`MODS` and :class:`RelatedItem`.'''
    XSD_SCHEMA = MODS_SCHEMA
    xmlschema = _mods_xmlschema

    title = xmlmap.StringField("mods:titleInfo/mods:title")
    resource_type  = xmlmap.SchemaField("mods:typeOfResource", "resourceTypeDefinition")
    name = xmlmap.NodeField('mods:name', Name)  # DEPRECATED: use names instead
    names = xmlmap.NodeListField('mods:name', Name)
    note = xmlmap.NodeField('mods:note', Note)
    origin_info = xmlmap.NodeField('mods:originInfo', OriginInfo)
    record_info = xmlmap.NodeField('mods:recordInfo', RecordInfo)
    identifiers = xmlmap.NodeListField('mods:identifier', Identifier)
    access_conditions = xmlmap.NodeListField('mods:accessCondition', AccessCondition)
    genres = xmlmap.NodeListField('mods:genre', Genre)
    languages = xmlmap.NodeListField('mods:language', Language)
    location = xmlmap.StringField('mods:location/mods:physicalLocation',
                                  required=False)
    subjects = xmlmap.NodeListField('mods:subject', Subject)

class RelatedItem(BaseMods):
    ''':class:`~eulxml.xmlmap.XmlObject` for MODS relatedItem: contains all the
    top-level MODS fields defined by :class:`BaseMods`, plus a type attribute.'''
    ROOT_NAME = 'relatedItem'
    # FIXME: schema required here for schemafields; this should be refactored
    XSD_SCHEMA = MODS_SCHEMA
    xmlschema = _mods_xmlschema
    #type = xmlmap.StringField('@type')
    type = xmlmap.SchemaField("@type", 'relatedItemTypeAttributeDefinition')

class MODS(BaseMods):
    '''Top-level :class:`~eulxml.xmlmap.XmlObject` for a MODS metadata record.
    Inherits all standard top-level MODS fields from :class:`BaseMods` and adds
    a mapping for :class:`RelatedItem`.
    '''
    ROOT_NAME = 'mods'
    XSD_SCHEMA = MODS_SCHEMA
    xmlschema = _mods_xmlschema
    related_items = xmlmap.NodeListField('mods:relatedItem', RelatedItem)


class MODSv34(MODS):
    ''':class:`~eulxml.xmlmap.XmlObject` for MODS version 3.4.  Currently
    consists of all the same fields as :class:`MODS`, but loads the MODS version
    3.4 schema for validation.
    '''
    XSD_SCHEMA = MODSv34_SCHEMA
    xmlschema = xmlmap.loadSchema(XSD_SCHEMA)
    # FIXME: how to set version attribute when creating from scratch?
