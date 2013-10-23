import logging
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from rdflib import URIRef

from eulfedora.models import Relation, ReverseRelation
from eulfedora.util import RequestFailed
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

# FIXME: what about this one ? emory-control:RushdieResearcherAllowed-1.0


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

    status_codes = {'processed': 'A', 'accessioned': 'I'}
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

    _deprecated_collection = Relation(relsext.isMemberOf, type=CollectionObject)
    ''':class:`~keep.collection.models.collection.v1_1.Collection` that this
    object is a member of, via `isMemberOf` relation.

    **deprecated** because these objects should be using **isMemberOfCollection**
    '''

    collection = Relation(relsext.isMemberOfCollection, type=CollectionObject)
    ''':class:`~keep.collection.models.CollectionObject that this object is a member of,
    via `isMemberOfCollection` relation.
    '''

    process_batch = ReverseRelation(relsext.hasMember, type=SimpleCollection)
    # access to the processing batch aka simple collection this object
    # is associated with; reverse because rel is stored on the simplecollection

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

    @property
    def content_md5(self):
        if self.filetech.content.file and self.filetech.content.file[0].md5:
            return self.filetech.content.file[0].md5


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
        if self._deprecated_collection:
            collection = self._deprecated_collection
        elif self.collection:
            collection = self.collection
        else:
            collection = None

        if collection and collection.exists:

            # collection_source_id
            if collection.mods.content.source_id is not None:  # allowed to be 0
                data['collection_source_id'] = collection.mods.content.source_id
            data['collection_id'] = collection.uri
            try:
                # pull parent & archive collection objects directly from fedora
                data['collection_label'] = collection.label
                # the parent collection of the collection this item belongs to is its archive
                if collection.collection:
                    data['archive_id'] = collection.collection.uri
                    data['archive_label'] = collection.collection.label

            except RequestFailed as rf:
                logger.error('Error accessing collection or archive object in Fedora: %s' % rf)

        # Arrangement unique id
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

        # get simple collections that have an association with this object
        try:
            simple_collections = repo.risearch.get_subjects(relsext.hasMember, self.uriref)
            simple_collections = list(simple_collections)

            sc_ids = []
            sc_labels = []

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
    CONTENT_MODELS = [boda.RushdieFile.RUSHDIE_FILE_CMODEL,
                      boda.Arrangement.ARRANGEMENT_CONTENT_MODEL]


class EmailMessage(boda.EmailMessage, ArrangementObject):
    CONTENT_MODELS = [boda.EmailMessage.EMAIL_MESSAGE_CMODEL,
                      boda.Arrangement.ARRANGEMENT_CONTENT_MODEL]

    NEW_OBJECT_VIEW = 'arrangement:view'

    @property
    def headers(self):
        '''
        Access CERP headers as a dictionary.
        '''
        return dict([(h.name, h.value) for h in self.cerp.content.headers])

    def email_label(self):
        '''
        Construct a label based on to, from, subject and date as
        stored in :attr:`EmailMessage.cerp.content`.

        Returns object label if set.
        '''
        if self.label:
            return self.label

        # if cerp is not present or has no data, return a generic label
        if not self.cerp or not self.cerp.content or \
            not self.cerp.content.from_list and not self.cerp.content.to_list:
            return 'Email message'

        # sender & to should generally be present
        if self.cerp.content.from_list:
            sender = self.cerp.content.from_list[0]
        else:
            sender = 'unknown sender'

        if self.cerp.content.to_list:
            to = self.cerp.content.to_list[0]
            if len(self.cerp.content.to_list) > 1:
                to = '%s et al.' % to
        else:
            to = 'unknown recipient'

        label = 'Email from %s to %s' % (sender, to)

        if self.cerp.content.subject_list:
            subject = self.cerp.content.subject_list[0]
            label += ' %s' % subject

        date = self.headers.get('Date', None)
        if date is not None:
            label += ' on %s' % date

        return label

    def index_data(self):
        '''Extend the :meth:`keep.arrangement.models.ArrangementObject.index_data` method to
        include additional data specific to EmailMessages objects.
        '''

        data = super(EmailMessage, self).index_data()
        data['label'] = self.email_label()
        # email does not have filetech or content; use mime data checksum
        # for content md5
        if self.mime_data.exists:
            data['content_md5'] = self.mime_data.checksum
            data['arrangement_id'] = self.mime_data.content.get('message-id')

        return data

    @property
    def content_md5(self):
        return self.mime_data.checksum

    @staticmethod
    def find_by_field(field, value, repo=None):
        '''
        Static method to find a single :class:`EmailMessage` by an indexed
        value.  Looks for the item in Solr and
        returns an :class:`EmailMessage` instance initialized
        from the repository if a single match is found for the
        requested field and value.

        Raises :class:`django.core.exceptions.MultipleObjectsReturned`
        if more than one match is found; raises
        :class:`django.core.exceptions.ObjectDoesNotExist` if no
        matches are found in the Solr index.

        :param field: solr field to search
        :param value: value to search on in the specified field

        :param repo: optional :class:`eulfedora.server.Repository`
            to use an existing connection with specific credentials

        :returns: :class:`EmailMessage`


        '''
        solr = solr_interface()
        search_terms = {
            field: value,
            'content_model': ArrangementObject.ARRANGEMENT_CONTENT_MODEL
        }
        q = solr.query(**search_terms).field_limit('pid')

        # check that we found one and only one
        found = len(q)
        # borrowing custom django exceptions for not found / too many
        # matches
        if found > 1:
            raise MultipleObjectsReturned('Found %d records with %s %s' % \
                                          (found, field, value))
        if not found:
            raise ObjectDoesNotExist('No record found with %s %s' % (field, value))

        if repo is None:
            repo = Repository()

        return repo.get_object(q[0]['pid'], type=EmailMessage)


    @staticmethod
    def by_checksum(md5sum, repo=None):
        '''
        Static method to find an :class:`EmailMessage` by the content
        md5 checksum.  Wrapper around :meth:`EmailMessage.find_by_field`.

        :param md5sum: MD5 checksum to search for
        '''
        return EmailMessage.find_by_field('content_md5', md5sum, repo=repo)

    @staticmethod
    def by_message_id(id, repo=None):
        '''
        Static method to find an :class:`EmailMessage` by its
        message id. Wrapper around :meth:`EmailMessage.find_by_field`.

        :param id: message id to search for
        '''
        return EmailMessage.find_by_field('arrangement_id', id, repo=repo)


class Mailbox(boda.Mailbox, ArrangementObject):
    CONTENT_MODELS = [ boda.Mailbox.MAILBOX_CONTENT_MODEL,
                       boda.Arrangement.ARRANGEMENT_CONTENT_MODEL ]

    NEW_OBJECT_VIEW = 'arrangement:view'
