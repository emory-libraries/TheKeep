import os
from rdflib import URIRef

from eulcore import xmlmap
from eulcore.fedora.models import FileDatastream, XmlDatastream, URI_HAS_MODEL

from digitalmasters.fedora import DigitalObject, Repository

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
    XSD_SCHEMA = "http://www.loc.gov/standards/mods/mods.xsd"
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
    XSD_SCHEMA = "http://www.loc.gov/standards/mods/mods.xsd"
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


class Modsv34(Mods):
    XSD_SCHEMA = "http://www.loc.gov/standards/mods/v3/mods-3-4.xsd" 
    xmlschema = xmlmap.loadSchema(XSD_SCHEMA)
    # FIXME: how to set version attribute when creating from scratch?

class CollectionMods(Mods):
    """Collection-specific MODS."""
    source_id = xmlmap.StringField("mods:identifier[@type='local_source_id']")
    # possibly map identifier type uri as well ?
    # TODO: (maybe) - single name here, multiple names on standard Mods
    # relatedItem type host - not editable on form, but may want mapping for easy access
    # - same for relatedItem type isReferencedyBy
    restrictions_on_access = xmlmap.NodeField('mods:accessCondition[@type="restrictions on access"]',
                                              ModsAccessCondition, instantiate_on_get=True)
    use_and_reproduction = xmlmap.NodeField('mods:accessCondition[@type="use and reproduction"]',
                                              ModsAccessCondition, instantiate_on_get=True)
    

class CollectionObject(DigitalObject):
    COLLECTION_CONTENT_MODEL = 'info:fedora/emory-control:Collection-1.1'
    CONTENT_MODELS = [ COLLECTION_CONTENT_MODEL ]

    # FIXME: there should be a better place to put this... (eulcore.fedora somewhere?)
    MEMBER_OF_COLLECTION = 'info:fedora/fedora-system:def/relations-external#isMemberOfCollection'

    mods = XmlDatastream('MODS', 'MODS Metadata', CollectionMods, defaults={
            'control_group': 'M',
            'format': Mods.ROOT_NS,
            'versionable': True,
        })

    _collection_id = None
    _collection_label = None

    def _update_dc(self):
        # FIXME: some duplicated logic from AudioObject save
        if self.mods.content.title:
            self.label = self.mods.content.title
            self.dc.content.title = self.mods.content.title
        if self.mods.content.resource_type:
            self.dc.content.type = self.mods.content.resource_type
        if self.mods.content.source_id or len(self.mods.content.identifiers):
            # remove all current dc identifiers and replace
            for i in range(len(self.dc.content.identifier_list)):
                self.dc.content.identifier_list.pop()
            self.dc.content.identifier_list.extend([id.text for id
                                            in self.mods.content.identifiers])
        if unicode(self.mods.content.name):
            # for now, use unicode conversion as defined in ModsName
            self.dc.content.creator_list[0] = unicode(self.mods.content.name)
        if len(self.mods.content.origin_info.created):                        
            self.dc.content.date = self.mods.content.origin_info.created[0].date
            # if a date range in MODS, add both dates
            if len(self.mods.content.origin_info.created) > 1:
                # if a date range in MODS, add both dates
                self.dc.content.date = "%s-%s" % (self.dc.content.date,
                            self.mods.content.origin_info.created[1].date)
            # FIXME: should this be dc:coverage ?

        # TEMPORARY: collection relation and cmodel must be in DC for find_objects
        # - these two can be removed once we implement gsearch
        if self.collection_id is not None:
            # store collection membership as dc:relation            
            self.dc.content.relation = self.collection_id
        # set collection content model URI as dc:format
        self.dc.content.format = self.COLLECTION_CONTENT_MODEL


    def save(self, logMessage=None):
        if self.mods.isModified() or self.rels_ext.isModified:
            # DC is derivative metadata based on MODS/RELS-EXT
            # if either has changed, update DC and object label to keep them in sync
            self._update_dc()

        return super(CollectionObject, self).save(logMessage)

    @property
    def collection_id(self):
        """Fedora URI for the top-level collection this object is a member of.
        :rtype: string
        """
        # for now, a collection should only have one isMemberOfCollection relation
        if self._collection_id is None:
            uri = self.rels_ext.content.value(subject=URIRef(self.uri),
                        predicate=URIRef(CollectionObject.MEMBER_OF_COLLECTION))
            if uri is not None:
                self._collection_id = str(uri)  # convert from URIRef to string
        return self._collection_id

    @property
    def collection_label(self):
        """Label of the top-level collection this object is a member of.
        :rtype: string
        """
        if self._collection_label is None:
            for coll in CollectionObject.top_level():
                if coll.uri == self.collection_id:
                    self._collection_label = coll.label
                    break
        return self._collection_label

    def set_collection(self, collection_uri):
        """Add or update the isMemberOfcollection relation in object RELS-EXT.
        
        :param collection_uri: string containing collection URI
        """
        # update/replace any existing collection membership (only one allowed, for now)
        self.rels_ext.content.set((
            URIRef(self.uri),
            URIRef(CollectionObject.MEMBER_OF_COLLECTION),
            URIRef(collection_uri)
        ))
        # clear out any cached collection id/label
        self._collection_id = None
        self._collection_label = None

    @staticmethod
    def top_level():
        """Find top-level collection objects.
        :returns: list of :class:`CollectionObject`
        :rtype: list
        """
        repo = Repository()
        # find all objects with cmodel collection-1.1 and no parents
        query = '''SELECT ?coll
        WHERE {
            ?coll <%(has_model)s> <%(cmodel)s>
            OPTIONAL { ?coll <%(member_of)s> ?parent }
            FILTER ( ! bound(?parent) )
        }
        ''' % {
            'has_model': URI_HAS_MODEL,
            'cmodel': CollectionObject.COLLECTION_CONTENT_MODEL,
            'member_of': CollectionObject.MEMBER_OF_COLLECTION
        }
        collections = repo.risearch.find_statements(query, language='sparql',
                                                         type='tuples', flush=True)
        return [repo.get_object(result['coll'], type=CollectionObject) for result in collections]

    def subcollections(self):
        """Find all sub-collections that are members of the current collection.

        :rtype: list of :class:`CollectionObject`
        """
        repo = Repository()
        # find all objects with cmodel collection-1.1 and this object for parent
        query = '''SELECT ?coll
        WHERE {
            ?coll <%(has_model)s> <%(cmodel)s> .
            ?coll <%(member_of)s> <%(parent)s>
        }
        ''' % {
            'has_model': URI_HAS_MODEL,
            'cmodel': CollectionObject.CONTENT_MODELS[0],
            'member_of': CollectionObject.MEMBER_OF_COLLECTION,
            'parent': self.uri,
        }
        collections = repo.risearch.find_statements(query, language='sparql',
                                                         type='tuples', flush=True)
        return [repo.get_object(result['coll'], type=CollectionObject) for result in collections]


class AudioObject(DigitalObject):
    CONTENT_MODELS = [ 'emory-control:EuterpeAudio-1.0' ]

    mods = XmlDatastream("MODS", "MODS Metadata", Mods, defaults={
            'control_group': 'M',
            'format': Mods.ROOT_NS,
            'versionable': True,
        })
    audio = FileDatastream("AUDIO", "Audio datastream", defaults={
            'mimetype': 'audio/x-wav',
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
    def init_from_file(filename, initial_label=None, request=None):
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
        :returns: :class:`AudioObject` initialized from thef ile
        '''
        if initial_label is None:
            initial_label = os.path.basename(filename)
        repo = Repository(request=request)
        obj = repo.get_object(type=AudioObject)
        # set initial object label from the base filename
        obj.label = initial_label
        obj.dc.content.title = obj.mods.content.title = obj.label
        obj.audio.content = open(filename)
        # set initial mods:typeOfResource - all AudioObjects default to sound recording
        obj.mods.content.resource_type = 'sound recording'

        return obj