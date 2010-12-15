from operator import attrgetter
import re

from rdflib import URIRef
from django.core.cache import cache

from eulcore import xmlmap
from eulcore.django.existdb.manager import Manager
from eulcore.django.existdb.models import XmlModel
from eulcore.fedora.rdfns import model as modelns
from eulcore.fedora.models import XmlDatastream
from eulcore.fedora.rdfns import relsext
from eulcore.xmlmap.eadmap import EncodedArchivalDescription, EAD_NAMESPACE

from digitalmasters import mods
from digitalmasters.fedora import DigitalObject, Repository


class CollectionMods(mods.MODS):
    """Collection-specific MODS, based on :class:`mods.MODS`."""
    source_id = xmlmap.IntegerField("mods:identifier[@type='local_source_id']")
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
    NEW_OBJECT_VIEW = 'collection:view'

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
            uri = self.rels_ext.content.value(subject=self.uriref,
                        predicate=relsext.isMemberOfCollection)
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

        if not isinstance(collection_uri, URIRef):
            collection_uri = URIRef(collection_uri)

        # update/replace any existing collection membership (only one allowed, for now)
        self.rels_ext.content.set((
            self.uriref,
            relsext.isMemberOfCollection,
            collection_uri
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
        cache_key = 'top-level-collection-pids'
        # these objects are not expected to change frequently - caching for an hour at a time
        # NOTE: could set a different cache duration for development environment, if useful
        cache_duration = 60*60
        # NOTE: can't pickle digital objects, so caching list of pids instead
        collection_pids = cache.get(cache_key, None)
        repo = Repository()
        if collection_pids is None:
            # find all objects with cmodel collection-1.1 and no parents
            query = '''SELECT ?coll
            WHERE {
                ?coll <%(has_model)s> <%(cmodel)s>
                OPTIONAL { ?coll <%(member_of)s> ?parent }
                FILTER ( ! bound(?parent) )
            }
            ''' % {
                'has_model': modelns.hasModel,
                'cmodel': CollectionObject.COLLECTION_CONTENT_MODEL,
                'member_of': relsext.isMemberOfCollection,
            }
            collection_pids = list(repo.risearch.find_statements(query, language='sparql',
                                                             type='tuples', flush=True))
            cache.set(cache_key, collection_pids, cache_duration)

        return [repo.get_object(result['coll'], type=CollectionObject) for result in collection_pids]

    @staticmethod
    def item_collections():
        """Find all collection objects that can contain items. Today this
        includes all those collections that are not top-level.
        :returns: list of :class:`CollectionObject`
        :rtype: list
        """
        repo = Repository()
        # find all objects with cmodel collection-1.1 and any parent
        query = '''SELECT DISTINCT ?coll
        WHERE {
            ?coll <%(has_model)s> <%(cmodel)s> .
            ?coll <%(member_of)s> ?parent
        }
        ''' % {
            'has_model': modelns.hasModel,
            'cmodel': CollectionObject.CONTENT_MODELS[0],
            'member_of': relsext.isMemberOfCollection,
        }
        collection_pids = repo.risearch.find_statements(query, language='sparql',
                                                        type='tuples', flush=True)
        collections = [ repo.get_object(result['coll'], type=CollectionObject)
                        for result in collection_pids ]
        return collections

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
            'has_model': modelns.hasModel,
            'cmodel': CollectionObject.CONTENT_MODELS[0],
            'member_of': relsext.isMemberOfCollection,
            'parent': self.uri,
        }
        collection_pids = repo.risearch.find_statements(query, language='sparql',
                                                         type='tuples', flush=True)
        collections = [repo.get_object(result['coll'], type=CollectionObject)
                                            for result in collection_pids]
        # for now, very simple sort on source identifier (MSS###)
        collections = sorted(collections, key=attrgetter('mods.content.source_id'))
        return collections



class FindingAid(XmlModel, EncodedArchivalDescription):
    """
    :class:`~eulcore.django.existdb.models.XmlModel` version of
    :class:`eulcore.xmlmap.eadmap.EncodedArchivalDescription`EAD object, for
    querying EAD content in an eXist DB.
    """
    ROOT_NAMESPACES = {
        'e': EAD_NAMESPACE,
    }
    # redeclaring namespace from eulcore to ensure prefix is correct for xpaths
    
    coverage = xmlmap.StringField('e:archdesc/e:did/e:unittitle/e:unitdate[@type="inclusive"]/@normal')
    # local repository *subarea* - e.g., MARBL, University Archives, Pitts
    repository = xmlmap.StringField('normalize-space(.//e:subarea)')

    objects = Manager('/e:ead')
    """:class:`eulcore.django.existdb.manager.Manager` - similar to an object manager
    for django db objects, used for finding and retrieving
    :class:`~digitalmasters.collection.models.FindingAid` objects from eXist.

    Configured to use */e:ead* as base search path.
    """

    def generate_collection(self):
        '''Generate a :class:`CollectionObject` with fields pre-populated
        based on the contents of the current Finding Aid object.
        '''
        repo = Repository()
        coll = repo.get_object(type=CollectionObject)
        # TODO: top-level collection membership?

        # title
        # remove trailing dates in these formats: , NNNN-NNN. , NNNN. , NNNN-
        # TODO: get rid of regex - use unittitle *without* any content inside unitdate (circa, bulk, etc)
        title = re.sub(r',\s*\d{4}-?(\d{4})?.?$', '', unicode(self.unittitle))        
        coll.mods.content.title = title  
        # main entry/name - origination, if any
        if self.archdesc.did.origination:
            name_text = unicode(self.archdesc.did.origination)
            # determine type of name
            type = self.archdesc.did.node.xpath('''local-name(e:origination/e:persname |
                e:origination/e:corpname  | e:origination/e:famname)''',
                namespaces=self.ROOT_NAMESPACES)
            if type == 'persname':
                name_type = 'personal'
            elif type == 'famname':
                name_type = 'family'
                # family names consistently end with a period, which can be removed
                name_text = name_text.rstrip('.')
            elif type == 'corpname':
                name_type = 'corporate'

            if name_type is not None:
                coll.mods.content.name.type = name_type
                
            authority = self.archdesc.did.node.xpath('string(e:origination/*/@source)',
                namespaces=self.ROOT_NAMESPACES)
            # lcnaf in the EAD is equivalent to naf in MODS
            if authority == 'lcnaf':
                coll.mods.content.name.authority = 'naf'

            coll.mods.content.name.name_parts.append(mods.NamePart(text=name_text))

        # date coverage
        if self.coverage:
            date_encoding = {'encoding': 'w3cdtf'}
            # date range
            if '/' in self.coverage:
                start, end = self.coverage.split('/')
                coll.mods.content.origin_info.created.append(mods.DateCreated(date=start,
                    point='start', key_date=True, **date_encoding))
                coll.mods.content.origin_info.created.append(mods.DateCreated(date=end,
                    point='end', **date_encoding))
            # single date
            else:
                coll.mods.content.origin_info.created.append(mods.DateCreated(date=self.coverage,
                    key_date=True, **date_encoding))

        # source id - numeric form of the manuscript/archive collection number
        coll.mods.content.source_id = self.archdesc.did.unitid.identifier

        # access restriction
        if self.archdesc.access_restriction:
            coll.mods.content.restrictions_on_access.text =  "\n".join([
                    unicode(c) for c in self.archdesc.access_restriction.content])

        # use & reproduction
        if self.archdesc.use_restriction:
            coll.mods.content.use_and_reproduction.text =  "\n".join([
                    unicode(c) for c in self.archdesc.use_restriction.content])

        # EAD url - where does this go?
        # accessible at self.eadid.url

        return coll


    @staticmethod
    def find_by_unitid(id, archive_name):
        '''Retrieve a single Finding Aid by top-level unitid and repository name.
        This method assumes a single Finding Aid should be found, so uses the
        :meth:`eulcore.existdb.query.QuerySet.get` method, which raises the following
        exceptions if anything other than a single match is found:
          * :class:`eulcore.existdb.exceptions.DoesNotExist` when no matches
             are found
          * :class:`eulcore.existdb.exceptions.ReturnedMultiple` if more than
             one match is found

        :param id: integer unitid to search on
        :param archive_name: name of the repository/subarea (numbering scheme)
        :returns: :class:`~digitalmasters.collection.models.FindingAid` instance
        '''
        return FindingAid.objects.filter(archdesc__did__unitid__identifier=id,
                repository=archive_name).get()

    
