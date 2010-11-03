from rdflib import URIRef

from eulcore import xmlmap
from eulcore.fedora.models import XmlDatastream, URI_HAS_MODEL

from digitalmasters import mods
from digitalmasters.fedora import DigitalObject, Repository


class CollectionMods(mods.MODS):
    """Collection-specific MODS, based on :class:`mods.MODS`."""
    source_id = xmlmap.StringField("mods:identifier[@type='local_source_id']")
    # possibly map identifier type uri as well ?
    # TODO: (maybe) - single name here, multiple names on standard MODS
    # relatedItem type host - not editable on form, but may want mapping for easy access
    # - same for relatedItem type isReferencedyBy
    restrictions_on_access = xmlmap.NodeField('mods:accessCondition[@type="restrictions on access"]',
                                              mods.AccessCondition, instantiate_on_get=True)
    use_and_reproduction = xmlmap.NodeField('mods:accessCondition[@type="use and reproduction"]',
                                              mods.AccessCondition, instantiate_on_get=True)



class CollectionObject(DigitalObject):
    COLLECTION_CONTENT_MODEL = 'info:fedora/emory-control:Collection-1.1'
    CONTENT_MODELS = [ COLLECTION_CONTENT_MODEL ]

    # FIXME: there should be a better place to put this... (eulcore.fedora somewhere?)
    MEMBER_OF_COLLECTION = 'info:fedora/fedora-system:def/relations-external#isMemberOfCollection'

    mods = XmlDatastream('MODS', 'MODS Metadata', CollectionMods, defaults={
            'control_group': 'M',
            'format': mods.MODS_NAMESPACE,
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
            # for now, use unicode conversion as defined in mods.Name
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
