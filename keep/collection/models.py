import logging
from rdflib import RDF

from django.conf import settings

from eulexistdb.manager import Manager
from eulexistdb.models import XmlModel
from eulfedora.models import XmlDatastream, Relation
from eulfedora.util import RequestFailed
from eulcm.models.collection.v1_1 import Collection
from eulcm.models.collection.v1_0 import Collection as Collectionv1_0
from eulcm.xmlmap.mods import MODS
from eulxml import xmlmap
from eulxml.xmlmap import mods
from eulxml.xmlmap.eadmap import EAD_NAMESPACE, EncodedArchivalDescription

from keep.common.fedora import ArkPidDigitalObject, Repository
from keep.common.rdfns import REPO
from keep.common.utils import solr_interface

logger = logging.getLogger(__name__)


class SimpleCollection(Collectionv1_0, ArkPidDigitalObject):
    '''This is a simple DC only collection  LIES
    '''

    NEW_OBJECT_VIEW = 'collection:simple_edit'

    # FIXME: why do we have mods on a dc-only collection ?
    mods = XmlDatastream('MODS', 'Descriptive Metadata (MODS)', MODS, defaults={
            'control_group': 'M',
            'format': mods.MODS_NAMESPACE,
            'versionable': True,
        })
    '''MODS :class:`~eulfedora.models.XmlDatastream` with content as
    :class:`eulxml.xmlmap.mods.MODS`; versionable, datastream ID
    ``MODS``'''

    type = Relation(RDF.type)

    # override this function and add additional functionality
    def __init__(self, *args, **kwargs):
        super(SimpleCollection, self).__init__(*args, **kwargs)

        # Only set type when creating a new object, as determined
        # by base class
        if self._create:
            self.type = REPO.SimpleCollection

    def index_data(self):
        '''Extend the default
        :meth:`eulfedora.models.DigitalObject.index_data`
        method to include additional fields specific to Keep
        SimpleCollection objects.'''
        # NOTE: we don't want to rely on other objects being indexed in Solr,
        # so index data should not use Solr to find any related object info

        # FIXME: is it worth splitting out descriptive index data here?
        data = super(SimpleCollection, self).index_data()
        data['object_type'] = 'collection'
        # FIXME: do we need to differentiate collection vs. simple collection ?

        if self.type:
            data['type'] = self.type

        return data

    @staticmethod
    def find_by_pid(pid):
        'Find a collection by pid and return a dictionary with collection information.'
        # NOTE: this method added as a replacement for
        # get_cached_collection_dict that was used elsewhere
        # throughout the site (audio app, etc.)  It should probably be
        # consolidated with other find methods...

        if pid.startswith('info:fedora/'):  # allow passing in uri
            pid = pid[len('info:fedora/'):]
        solr = solr_interface()
        solrquery = solr.query(content_model=SimpleCollection.COLLECTION_CONTENT_MODEL,
                               pid=pid)
        result = solrquery.execute()
        if len(result) == 1:
            return result[0]

    @staticmethod
    def simple_collections():
        """Find all simpleCollection objects in the configured Fedora
        pidspace that can contain items.

        :returns: list of dict
        :rtype: list
        """

        # search solr for simpleCollection objects
        solr = solr_interface()
        solrquery = solr.query(content_model=SimpleCollection.COLLECTION_CONTENT_MODEL, \
                    type=REPO.SimpleCollection)

        # by default, only returns 10; get everything
        # - solr response is a list of dictionary with collection info
        # use dictsort and regroup in templates for sorting where appropriate
        return solrquery.paginate(start=0, rows=1000).execute()


class CollectionObject(Collection, ArkPidDigitalObject):
    '''Fedora Collection Object.  Extends :class:`~eulfedora.models.DigitalObject`.
    This really represents an archival collection
    '''

    NEW_OBJECT_VIEW = 'collection:view'

    _archives = None

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
        if self.mods.content.name and unicode(self.mods.content.name):
            # for now, use unicode conversion as defined in mods.Name
            self.dc.content.creator_list[0] = unicode(self.mods.content.name)
        if self.mods.content.origin_info and \
                len(self.mods.content.origin_info.created):
            self.dc.content.date = self.mods.content.origin_info.created[0].date
            # if a date range in MODS, add both dates
            if len(self.mods.content.origin_info.created) > 1:
                # if a date range in MODS, add both dates
                self.dc.content.date = "%s-%s" % (self.dc.content.date,
                            self.mods.content.origin_info.created[1].date)
            # FIXME: should this be dc:coverage ?

    def save(self, logMessage=None):
        '''Save the object.  If the content of the MODS or RELS-EXT datastreams
        have been changed, the DC will be updated and saved as well.

        :param logMessage: optional log message
        '''
        if self.mods.isModified() or self.rels_ext.isModified:
            # DC is derivative metadata based on MODS/RELS-EXT
            # if either has changed, update DC and object label to keep them in sync
            self._update_dc()

        return super(CollectionObject, self).save(logMessage)

    @staticmethod
    def archives(format=None):
        """Find Archives objects, to which CollectionObjects belong.

        :returns: list of :class:`CollectionObject`
        :rtype: list
        """
        # NOTE: formerly called top-level collections or Repository /
        # Owning Repository; should now be called archive and labeled
        # as such anywhere user-facing

        # TODO: search logic very similar to item_collections and
        # subcollections methods; consider refactoring search logic
        # into a common search method.

        if CollectionObject._archives is None:
            # find all objects with cmodel collection-1.1 and no parents

            # search solr for collection objects with NO parent collection id
            solr = solr_interface()
            # NOTE: not filtering on pidspace, since top-level objects are loaded as fixtures
            # and may not match the configured pidspace in a dev environment
            solrquery = solr.query(content_model=CollectionObject.COLLECTION_CONTENT_MODEL)
            collections = solrquery.exclude(archive_id__any=True).sort_by('title_exact').execute()
            # store the solr response format
            CollectionObject._archives = collections

        if format == dict:
            return CollectionObject._archives

        # otherwise, initialize as instances of CollectionObject
        repo = Repository()
        return [repo.get_object(arch['pid'], type=CollectionObject)
                                                       for arch in CollectionObject._archives]

    @staticmethod
    def find_by_pid(pid):
        'Find a collection by pid and return a dictionary with collection information.'
        # NOTE: this method added as a replacement for
        # get_cached_collection_dict that was used elsewhere
        # throughout the site (audio app, etc.)  It should probably be
        # consolidated with other find methods...

        if pid.startswith('info:fedora/'):  # allow passing in uri
            pid = pid[len('info:fedora/'):]
        solr = solr_interface()
        solrquery = solr.query(content_model=CollectionObject.COLLECTION_CONTENT_MODEL,
                               pid=pid)
        result = solrquery.execute()
        if len(result) == 1:
            return result[0]
        # otherwise - exception? not found / too many

    @staticmethod
    def item_collections():
        """Find all collection objects in the configured Fedora
        pidspace that can contain items. Today this includes all
        collections that belong to arn archive.

        :returns: list of dict
        :rtype: list
        """

        # search solr for collection objects with NO parent collection id
        solr = solr_interface()
        solrquery = solr.query(content_model=CollectionObject.COLLECTION_CONTENT_MODEL,
                               archive_id__any=True)
        # by default, only returns 10; get everything
        # - solr response is a list of dictionary with collection info
        # use dictsort and regroup in templates for sorting where appropriate
        return solrquery.paginate(start=0, rows=1000).execute()

    def subcollections(self):
        """Find all sub-collections that are members of the current collection
        in the configured Fedora pidspace.

        :rtype: list of dict
        """
        solr = solr_interface()
        solrquery = solr.query(content_model=CollectionObject.COLLECTION_CONTENT_MODEL,
                               pid='%s:' % settings.FEDORA_PIDSPACE,
                               archive_id=self.pid)
        # by default, only returns 10; get everything
        # - solr response is a list of dictionary with collection info
        # use dictsort in template for sorting where appropriate
        return solrquery.paginate(start=0, rows=1000).execute()

    @staticmethod
    def find_by_collection_number(num, parent=None):
        '''Find a CollectionObject in Fedora by collection number (or
        source id), optionally limited by parent collection (owning
        archive).

        :param num: collection number to search for (aka source id)
        :param parent: optional; archive that the collection must belong to
        :return: generator of any matching items, as instances of
            :class:`CollectionObject`
        '''
        solr = solr_interface()
        solrquery = solr.query(content_model=CollectionObject.COLLECTION_CONTENT_MODEL,
                               pid='%s:*' % settings.FEDORA_PIDSPACE,
                               source_id=int(num))
        # if parent is specified, restrict by archive id (parent should be a pid)
        if parent is not None:
            solrquery = solrquery.query(archive_id=parent)
        # by default, only returns 10; get everything
        # - solr response is a list of dictionary with collection info
        # use dictsort in template for sorting where appropriate
        collections = solrquery.paginate(start=0, rows=1000).execute()

        # return a generator of matching items, as instances of CollectionObject
        repo = Repository()
        for coll in collections:
            yield repo.get_object(coll['pid'], type=CollectionObject)

    def index_data_descriptive(self):
        '''Extend the default
        :meth:`eulfedora.models.DigitalObject.index_data_descriptive`
        method to include a few additional fields specific to Keep
        Collection objects.'''

        data = super(CollectionObject, self).index_data_descriptive()
        data['object_type'] = 'collection'
        if self.collection:
            data.update(self._index_data_archive())

        # if source id is set, include it
        if self.mods.content.source_id is not None:
            data['source_id'] = self.mods.content.source_id

        if self.mods.content.ark_uri:
            data['ark_uri'] = self.mods.content.ark_uri

        return data

    def _index_data_archive(self):
        data = {}
        archive = self.collection
        if archive is not None:
            data['archive_id'] = archive.uri
            try:
                data['archive_label'] = archive.label
                data['archive_short_name'] = archive.mods.content.short_name
            except RequestFailed as rf:
                logger.error('Error accessing archive object %s in Fedora: %s' % \
                             (self.collection.pid, rf))
        return data


class FindingAid(XmlModel, EncodedArchivalDescription):
    """
    This is an :class:`~eulexistdb.models.XmlModel` version of
    :class:`~eulxml.xmlmap.eadmap.EncodedArchivalDescription` (EAD) object, to
    simplify querying for EAD content in an eXist DB.
    """
    ROOT_NAMESPACES = {
        'e': EAD_NAMESPACE,
    }
    # redeclaring namespace from eulxml to ensure prefix is correct for xpaths

    coverage = xmlmap.StringField('e:archdesc/e:did/e:unittitle/e:unitdate[@type="inclusive"]/@normal')
    # local repository *subarea* - e.g., MARBL, University Archives, Pitts
    repository = xmlmap.StringField('normalize-space(.//e:subarea)')

    objects = Manager('/e:ead')
    """:class:`eulexistdb.manager.Manager` - similar to an object manager
    for django db objects, used for finding and retrieving
    :class:`~keep.collection.models.FindingAid` objects from eXist.

    Configured to use */e:ead* as base search path.
    """

    def generate_collection(self):
        '''Generate a :class:`CollectionObject` with fields pre-populated
        based on the contents of the current Finding Aid object.
        '''
        repo = Repository()
        coll = repo.get_object(type=CollectionObject)
        # TODO: archive membership?

        # title - using 'short' form without unitdate, stripping any trailing whitespace & . or ,
        # TODO/FIXME: does NOT work for unittitles with nested tags, e.g. title - see pomerantz
        coll.mods.content.title = unicode(self.unittitle.short).rstrip().rstrip('.,')
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
                coll.mods.content.create_name()
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
            coll.mods.content.create_origin_info()
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
            coll.mods.content.create_restrictions_on_access()
            coll.mods.content.restrictions_on_access.text = "\n".join([
                    unicode(c) for c in self.archdesc.access_restriction.content])

        # use & reproduction
        if self.archdesc.use_restriction:
            coll.mods.content.create_use_and_reproduction()
            coll.mods.content.use_and_reproduction.text = "\n".join([
                    unicode(c) for c in self.archdesc.use_restriction.content])

        # EAD url - where does this go?
        # accessible at self.eadid.url

        return coll

    @staticmethod
    def find_by_unitid(id, archive_name):
        '''Retrieve a single Finding Aid by archive unitid and repository name.
        This method assumes a single Finding Aid should be found, so uses the
        :meth:`eulexistdb.query.QuerySet.get` method, which raises the following
        exceptions if anything other than a single match is found:

          * :class:`eulexistdb.exceptions.DoesNotExist` when no matches
            are found
          * :class:`eulexistdb.exceptions.ReturnedMultiple` if more than
            one match is found

        :param id: integer unitid to search on
        :param archive_name: name of the repository/subarea (numbering scheme)
        :returns: :class:`~keep.collection.models.FindingAid` instance
        '''
        return FindingAid.objects.filter(archdesc__did__unitid__identifier=id,
                repository=archive_name).get()

