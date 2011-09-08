from django.db import models

from eulfedora.models import FileDatastream, XmlDatastream
from eulxml import xmlmap
from eulfedora.rdfns import relsext

from keep import mods
from keep.common.fedora import DigitalObject, Repository
from keep.common.models import Rights, FileMasterTech

from keep.collection.models import CollectionObject
from rdflib import URIRef

class Permissions(models.Model):
    class Meta:
        permissions = (
            ("marbl_allowed", "Access to MARBL collections is allowed."),
        )

class Series_Base(mods.RelatedItem):

    uri = xmlmap.StringField('mods:identifier[@type="uri"]',
            required=False, verbose_name='URI Identifier')

    base_ark = xmlmap.StringField('mods:identifier[@type="base_ark"]',
            required=False, verbose_name='base ark target of document')

    full_id = xmlmap.StringField('mods:identifier[@type="full_id"]',
            required=False, verbose_name='full id of this node')

    short_id = xmlmap.StringField('mods:identifier[@type="short_id"]',
            required=False, verbose_name='short id of this node')

class Series2(Series_Base):
    series = xmlmap.NodeField("mods:relatedItem[@type='series']", Series_Base,
        required=False,
        help_text='subseries')

class Series1(Series_Base):
    series = xmlmap.NodeField("mods:relatedItem[@type='series']", Series2,
        required=False,
        help_text='subseries')

class ArrangementMods(mods.MODS):
    series = xmlmap.NodeField("mods:relatedItem[@type='series']", Series1,
        required=False,
        help_text='series')

class ArrangementObject(DigitalObject):
    ARRANGEMENT_CONTENT_MODEL = 'info:fedora/emory-control:Arrangement-1.0'
    CONTENT_MODELS = [ ARRANGEMENT_CONTENT_MODEL ]
    NEW_OBJECT_VIEW = 'arrangement:edit'

    rights = XmlDatastream("Rights", "Usage rights and access control metadata", Rights,
        defaults={
            'control_group': 'M',
            'versionable': True,
        })
    '''access control metadata :class:`~eulfedora.models.XmlDatastream`
    with content as :class:`Rights`'''

    filetech = XmlDatastream("FileMasterTech", "File Technical Metadata", FileMasterTech ,defaults={
            'control_group': 'M',
            'versionable': True,
        })

    mods = XmlDatastream('MODS', 'MODS Metadata', ArrangementMods, defaults={
            'control_group': 'M',
            'format': mods.MODS_NAMESPACE,
            'versionable': True,
        })
    'MODS :class:`~eulfedora.models.XmlDatastream` with content as :class:`ArrangementMods`'

    _collection_uri = None

    def index_data(self):
        '''Extend the default
        :meth:`eulfedora.models.DigitalObject.index_data`
        method to include additional fields specific to Keep
        Arrangement objects.'''
        # NOTE: we don't want to rely on other objects being indexed in Solr,
        # so index data should not use Solr to find any related object info


        # FIXME: is it worth splitting out descriptive index data here?
        data = super(ArrangementObject, self).index_data()

        print 'THIS SHOULD EXIST: %s' % (self.collection_uri)
        if self.collection_uri is not None:
            
            data['collection_id'] = self.collection_uri
            try:
                # pull parent & archive collection objects directly from fedora
                parent = CollectionObject(self.api, self.collection_uri)
                data['collection_label'] = parent.label
                # the parent collection of the collection this item belongs to is its archive
                # FIXME: CollectionObject uses collection_id where AudioObject uses collection_uri
                data['archive_id'] = parent.collection_id
                archive = CollectionObject(self.api, parent.collection_id)
                data['archive_label'] = archive.label
            except RequestFailed as rf:
                logger.error('Error accessing collection or archive object in Fedora: %s' % rf)
            
        # rights access status code
        if self.rights.content.access_status:
            data['access_code'] = self.rights.content.access_status.code
            
        return data


    def _get_collection_uri(self):
        # for now, an arrangement object should only have one isMemberOfCollection relation
        if self._collection_uri is None:
            self._collection_uri = self.rels_ext.content.value(
                        subject=self.uriref,
                        predicate=relsext.isMemberOfCollection)
        return self._collection_uri

    def _set_collection_uri(self, collection_uri):
        # TODO: handle None!!!  don't set to rdflib.term.URIRef('None')), clear out rels-ext
        if collection_uri is None:

            # remove the current collection membership 
            self.rels_ext.content.remove((
                self.uriref,
                relsext.isMemberOfCollection,
                self._collection_uri))
            
            # clear out any cached collection id
            self._collection_uri = None

        else:
            if not isinstance(collection_uri, URIRef):
                collection_uri = URIRef(collection_uri)

            # update/replace any existing collection membership (only one allowed, for now)
            self.rels_ext.content.set((
                self.uriref,
                relsext.isMemberOfCollection,
                collection_uri))
            # clear out any cached collection id
            self._collection_uri = None

    # FIXME: CollectionObject has an equivalent property called
    # collection_id; should these be consisent? common code?
    collection_uri = property(_get_collection_uri, _set_collection_uri)
    ':class:`~rdflib.URIRef` for the collection this object belongs to'



