import logging
from django.db import models
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from eulfedora.models import FileDatastream, XmlDatastream, Relation
from eulfedora.util import RequestFailed
from eulxml import xmlmap
from eulxml.xmlmap import mods
from eulfedora.rdfns import relsext

from eulcm.models import boda


from keep.collection.models import SimpleCollection
from keep.common.fedora import ArkPidDigitalObject, Repository
from keep.common.utils import solr_interface

from keep.collection.models import CollectionObject
from rdflib import URIRef

logger = logging.getLogger(__name__)



class ArrangementObject(boda.Arrangement, ArkPidDigitalObject):
    '''Subclass of :class:`eulfedora.models.DigitalObject` for
    "arrangement" content.'''

    NEW_OBJECT_VIEW = 'arrangement:edit'

    component_key = {
        'FileMasterTech': 'file technical metadata',
        'MODS': 'descriptive metadata',
        'DC': 'descriptive metadata',
        'Rights': 'rights metadata',
        'RELS-EXT': 'collection membership',  # TODO: revise when/if we add more relations
    }

    def index_data(self):
        '''Extend the default
        :meth:`eulfedora.models.DigitalObject.index_data` method to
        include additional fields specific to Keep Arrangement
        objects.  Includes collection and archive information, along
        with arrangement id and access status.'''
        # NOTE: we don't want to rely on other objects being indexed in Solr,
        # so index data should not use Solr to find any related object info
        
        repo = Repository()   # FIXME: use relation from current object instead

        # FIXME: is it worth splitting out descriptive index data here?
        data = super(ArrangementObject, self).index_data()

        data['object_type'] = 'born-digital'  # ??

        
        # Collection Info
        # TODO: can we use Relation to improve this?
        collection = list(self.rels_ext.content.objects(self.uriref, relsext.isMemberOf))
        if collection:
            data['collection_id'] = collection[0]

            try:
                # pull parent & archive collection objects directly from fedora
                parent = CollectionObject(self.api, collection[0])
                data['collection_label'] = parent.label
                # the parent collection of the collection this item belongs to is its archive
                # FIXME: CollectionObject uses collection_id where AudioObject uses collection_uri
                if parent.collection:
                    data['archive_id'] = parent.collection.uri
                    data['archive_label'] = parent.collection.label

            except RequestFailed as rf:
                logger.error('Error accessing collection or archive object in Fedora: %s' % rf)
            

        #Arrangement unique id
        try:
            if self.filetech.content.file:
                if self.filetech.content.file[0].local_id:
                    data["arrangement_id"] = self.filetech.content.file[0].local_id
                if self.filetech.content.file[0].md5:
                    data['content_md5'] = self.filetech.content.file[0].md5
        except Exception as e:
            logging.error("Error getting arrangement id or content MD5 for %s: %s" % self.pid, e)

        # rights access status code
        if self.rights.content.access_status:
            data['access_code'] = self.rights.content.access_status.code
            # normally this should be picked up via dc:rights, but arrangement
            # objects don't seem to have DC fields populated
            # NOTE: migrated items don't seem to have rights text set
            if self.rights.content.access_status.text:
                data['rights'] = self.rights.content.access_status.text


        #get simple collections that have an association with this object
        try:
            simple_collections = repo.risearch.get_subjects(relsext.hasMember, self.uriref)
            simple_collections =list(simple_collections)

            sc_ids =[]
            sc_labels =[]

            for sc in simple_collections:
                obj = repo.get_object(pid=sc, type=repo.infer_object_subtype)
                if isinstance(obj, SimpleCollection):
                    sc_ids.append("info:fedora/%s" % obj.pid)
                    sc_labels.append(obj.label)
        except RequestFailed as rf:
            logger.error('Error accessing simpleCollection in Fedora: %s' % rf)

        if sc_ids:
            data["simpleCollection_id"] = sc_ids
        if sc_labels:
            data["simpleCollection_label"] = sc_labels

            


        return data
        

    @staticmethod
    def by_arrangement_id(id, repo=None):
        '''
        Static method to find an :class:`ArrangementObject` by its
        local or arrangement id.  Looks for the item in Solr and
        returns an :class:`ArrangementObject` instance initialized
        from the repository if a single match is found for the
        requested id.

        Raises :class:`django.core.exceptions.MultipleObjectsReturned`
        if more than one match is found; raises
        :class:`django.core.exceptions.ObjectDoesNotExist` if no
        matches are found in the Solr index.

        :param id: arrangement id or local id
        
        :param repo: optional :class:`eulfedora.server.Repository`
            to use an existing connection with specific credentials
            
        :returns: :class:`ArrangementObject` 
    
        
        '''
        solr = solr_interface()
        q = solr.query(arrangement_id=id,
                   content_model=ArrangementObject.ARRANGEMENT_CONTENT_MODEL) \
                   .field_limit('pid')

        # check that we found one and only one
        found = len(q)
        # borrowing custom django exceptions for not found / too many
        # matches
        if found > 1:
            raise MultipleObjectsReturned('Found %d records with arrangement id %s' % \
                                          (found, id))
        if not found:
            raise ObjectDoesNotExist('No record found with arrangement id %s' % id)

        if repo is None:
            repo = Repository()
            
        return repo.get_object(q[0]['pid'], type=ArrangementObject)


class RushdieArrangementFile(boda.RushdieFile, ArrangementObject):
    CONTENT_MODELS = [ boda.RushdieFile.RUSHDIE_FILE_CMODEL,
                       boda.Arrangement.ARRANGEMENT_CONTENT_MODEL ] 


class EmailMessage(boda.EmailMessage, ArrangementObject):
    CONTENT_MODELS = [ boda.EmailMessage.EMAIL_MESSAGE_CMODEL,
                       boda.Arrangement.ARRANGEMENT_CONTENT_MODEL ] 

class Mailbox(boda.Mailbox, ArrangementObject):
    CONTENT_MODELS = [ boda.Mailbox.MAILBOX_CONTENT_MODEL,
                       boda.Arrangement.ARRANGEMENT_CONTENT_MODEL ] 
