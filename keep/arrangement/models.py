import logging
from django.db import models
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from rdflib import URIRef

from eulfedora.models import FileDatastream, XmlDatastream, Relation
from eulfedora.util import RequestFailed
from eulxml import xmlmap
from eulxml.xmlmap import mods
from eulfedora.rdfns import relsext, model as modelns
from eulcm.models import boda

from keep.collection.models import SimpleCollection
from keep.common.fedora import ArkPidDigitalObject, Repository
from keep.common.utils import solr_interface
from keep.collection.models import CollectionObject

logger = logging.getLogger(__name__)


# content models currently used for xacml access / restriction
ACCESS_ALLOWED_CMODEL = "info:fedora/emory-control:ArrangementAccessAllowed-1.0"
ACCESS_RESTRICTED_CMODEL = "info:fedora/emory-control:ArrangementAccessRestricted-1.0"


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

    status_codes = {'processed': 'A', 'accessioned' : 'I'}
    # map arrangement status to fedora object state

    def _get_arrangement_status(self):
        for status, code in self.status_codes.iteritems():
            if self.state == code:
                return status
            
    def _set_arrangement_status(self, status):
        if status not in self.status_codes:
            raise ValueError('%s is not a recognized arrangement status' % status)
        self.state = self.status_codes[status]
        
    arrangement_status = property(_get_arrangement_status, _set_arrangement_status)
    'arrangement status, i.e., whether this item is processed or accessioned'

    
    def save(self, logMessage=None):
        '''Save the object.  If the content of the rights datastream
        has changed, update content models used to control access to
        match the current rights access code.

        :param logMessage: optional log message
        '''
        if self.rights.isModified:
            self._update_access_cmodel()

        return super(ArrangementObject, self).save(logMessage)


    def _update_access_cmodel(self):
        # update access/restriction content models based on rights access code
        
        # FIXME: is there not a better way to add/remove cmodels ? 
        _allowed_triple = (self.uriref, modelns.hasModel, URIRef(ACCESS_ALLOWED_CMODEL))
        _restricted_triple = (self.uriref, modelns.hasModel, URIRef(ACCESS_RESTRICTED_CMODEL))
        
        if self.rights.content.access_status and \
           self.rights.content.access_status.code == '2':
            # FIXME: sholudn't have to hard code this number;
            # can we use researcher_access check instead ? 

            # allow access.
            # remove restricted if present, add allowed if not present
            if _restricted_triple in self.rels_ext.content:
                self.rels_ext.content.remove(_restricted_triple)
            if _allowed_triple not in self.rels_ext.content:
                self.rels_ext.content.add(_allowed_triple)

        else:
            # deny access.
            # remove allowed if present, add restricted if not present
            if _allowed_triple in self.rels_ext.content:
                self.rels_ext.content.remove(_allowed_triple)
            if _restricted_triple not in self.rels_ext.content:
                self.rels_ext.content.add(_restricted_triple)


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
