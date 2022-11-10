from datetime import datetime
import logging
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db import models
import os
from rdflib import URIRef
import tempfile
import uuid
import urllib.request as urllib2

from eulfedora.models import Relation, ReverseRelation, XmlDatastream
from eulfedora.util import RequestFailed
from eulfedora.rdfns import relsext, model as modelns
from eulcm.models import boda
from eulcm.xmlmap.boda import ArrangementMods
from eulcm.xmlmap.mods import MODS
from eulxml import xmlmap
from eulxml.xmlmap import premis, mods
from pidservices.djangowrapper.shortcuts import DjangoPidmanRestClient

from keep import __version__
from keep.collection.models import SimpleCollection
from keep.common.models import PremisFixity, PremisObject, PremisEvent
from keep.common.fedora import ArkPidDigitalObject, Repository
from keep.common.utils import solr_interface
from keep.collection.models import CollectionObject
from keep.file.utils import sha1sum


logger = logging.getLogger(__name__)

# content models currently used for xacml access / restriction
ACCESS_ALLOWED_CMODEL = "info:fedora/emory-control:ArrangementAccessAllowed-1.0"
ACCESS_RESTRICTED_CMODEL = "info:fedora/emory-control:ArrangementAccessRestricted-1.0"

# try to configure a pidman client to get pids.
try:
    pidman = DjangoPidmanRestClient()
except:
    # if we're in dev mode then we can fall back on the fedora default
    # pid allocator. in non-dev, though, we really need pidman
    if getattr(settings, 'DEV_ENV', False):
        pidman = None
    else:
        raise

# FIXME: what about this one ? emory-control:RushdieResearcherAllowed-1.0


class Arrangement(models.Model):
    'Place-holder DB model to define permissions for "arrangement" objects'
    class Meta:
        permissions = (
            ("view_arrangement", "Can view, search, and browse arrangement objects"),
        )


class ArrangementPremis(premis.Premis):
    # adapdet from diskimage premis
    XSD_SCHEMA = premis.PREMIS_SCHEMA

    object = xmlmap.NodeField('p:object', PremisObject)

    events = xmlmap.NodeListField('p:event', PremisEvent)


class LocalArrangementMods(ArrangementMods, MODS):
    # extend eulcml arrangement mods to include eulcm mods with
    # mappings for identifiers, ark and ark uri
    pass


class ArrangementObject(boda.Arrangement, ArkPidDigitalObject):
    '''Subclass of :class:`eulfedora.models.DigitalObject` for
    "arrangement" content.'''

    NEW_OBJECT_VIEW = 'arrangement:edit'

    mods = XmlDatastream('MODS', 'MODS Metadata', LocalArrangementMods,
        defaults={
            'control_group': 'M',
            'format': mods.MODS_NAMESPACE,
            'versionable': True,
    })
    '''MODS :class:`~eulfedora.models.XmlDatastream` with content as
    :class:`ArrangementMods`; datstream ID ``MODS``'''


    provenance = XmlDatastream(
        'provenanceMetadata', 'Provenance metadata',
        ArrangementPremis, defaults={'versionable': False})

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
        for status, code in self.status_codes.items():
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

    def get_original_datastream(self):
        # retrieve original datastream object; used to generate
        # object information for premis checksums
        orig_ds = self.getDatastreamObject('ORIGINAL')
        if orig_ds.exists:
            return orig_ds

        # for email content, use MIME datastream as original content
        orig_ds = self.getDatastreamObject('MIME')
        if orig_ds.exists:
            return orig_ds

        # TODO: what to do for email folders ?

        raise Exception('No original datastream found')


    def set_premis_object(self):
        # NOTE: could add a check to see if premis exists before setting
        # these values (although we don't expect arrangment objects
        # to have premis by default)

        # NOTE: should be using the ark:/####/#### id form here
        # using ArkPidDigitalObject ark property
        self.provenance.content.create_object()
        self.provenance.content.object.id_type = 'ark'
        self.provenance.content.object.id = self.mods.content.ark

        # add basic object premis information
        # object type required to be schema valid, must be in premis namespace
        self.provenance.content.object.type = 'p:file'
        self.provenance.content.object.composition_level = 0

        original_ds = self.get_original_datastream()

        # add MD5 and SHA-1 checksums for original datastream content
        # Fedora should already have an MD5
        # (NOTE: could confirm that this is MD5 using checksum_type)
        self.provenance.content.object.checksums.append(PremisFixity(algorithm='MD5'))
        self.provenance.content.object.checksums[0].digest = original_ds.checksum

        # save original content to disk in order to calculate a SHA-1 checkusum
        # don't delete when file handle is closed
        origtmpfile = tempfile.NamedTemporaryFile(
            prefix='%s-orig-' % self.noid, delete=False)
        for data in original_ds.get_chunked_content():
            origtmpfile.write(data)

        # close to flush contents before calculating checksum
        origtmpfile.close()

        # calculate SHA-1 and add to premis
        self.provenance.content.object.checksums.append(PremisFixity(algorithm='SHA-1'))
        self.provenance.content.object.checksums[1].digest = sha1sum(origtmpfile.name)

        # clean up temporary copy of the original file
        os.remove(origtmpfile.name)

        # set object format - using original file mimetype
        self.provenance.content.object.create_format()
        self.provenance.content.object.format.name = original_ds.mimetype

    def identifier_change_event(self, oldpid):
        '''Add an identifier change event to the premis for this object.'''

        detail_msg = 'Persistent identifier reassigned from %s to %s' % \
            (oldpid, self.pid)
        idchange_event = PremisEvent()
        idchange_event.id_type = 'UUID'
        idchange_event.id = uuid.uuid1()
        idchange_event.type = 'identifier assignment'
        idchange_event.date = datetime.now().isoformat()
        idchange_event.detail = 'program="keep"; version="%s"' % __version__
        idchange_event.outcome = 'Pass'
        idchange_event.outcome_detail = detail_msg
        idchange_event.agent_type = 'fedora user'
        idchange_event.agent_id = self.api.username
        self.provenance.content.events.append(idchange_event)

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

    def update_ark_label(self, force_update=False):
        """Update an object's label. While arrangement objects do have a MODS datastream,
        the descriptive metadata about the object (including title) is currently stored
        in the DC (or Dublin Core). In Fedora the DC data stream is a special one that
        always exists, and we do not need to check if the dc exists. This method will compare
        the title in DC field in Fedora and that in the Pidman object.

        :param force_update: optional flag that will enforce update of the object title
            regardless of mods.isModified(), when supplied as True
        """

        # Check if the object itself exists, and proceed if so.
        # Python evaluates conditionals from left to right; therefore the
        # order here matters
        if self.exists:
            # perform update when either force_update flag is provided, or otherwise
            # only take actions when mods is modified.
            if force_update or self.dc.isModified():
                if pidman is not None:
                    try:
                        pidman_label = pidman.get_ark(self.noid)['name']
                        if self.dc.content.title != pidman_label: # when the title is different
                            pidman.update_ark(noid=self.noid, name=self.dc.content.title)

                    # catch KeyError
                    except KeyError as e:
                        logger.error("Object %s doesn't have a name attribute in Pidman.", self.noid)

                    # catch HTTPError (e.g. 401, 404)
                    except urllib2.HTTPError as e:
                        logger.error("Object %s errored out in Pidman HTTP requests. \
                            HTTP status code: %s \n", self.noid, str(e.code))

                    # catch other exceptions
                    except Exception as e:
                        logger.error("Object %s errored out in Pidman. \
                            Error message: %s \n", self.noid, str(e))
                else:
                    logging.warning("Pidman client does not exist.")

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

        if self.has_model(boda.EmailMessage.EMAIL_MESSAGE_CMODEL) or \
          self.has_model(boda.Mailbox.MAILBOX_CONTENT_MODEL):
            data['object_type'] = 'email'
        # elif self.has_model(boda.RushdieFile.RUSHDIE_FILE_CMODEL):
            # data['object_type'] = 'file'
        else:
            # generic fallback
            data['object_type'] = 'born-digital'

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
            data['collection_id'] = collection.pid
            try:
                # pull parent & archive collection objects directly from fedora
                data['collection_label'] = collection.label
                # the parent collection of the collection this item belongs to is its archive

                # FIXME: this shouldn't be indexed here; are we actually
                # using it anywhere?
                # if collection.collection:
                #     data['archive_id'] = collection.collection.uri
                #     data['archive_label'] = collection.collection.label

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


class Mailbox(boda.Mailbox, ArrangementObject):
    CONTENT_MODELS = [boda.Mailbox.MAILBOX_CONTENT_MODEL,
                      boda.Arrangement.ARRANGEMENT_CONTENT_MODEL]

    NEW_OBJECT_VIEW = 'arrangement:view'

    # note: mailbox lists email messages in rels-ext


class EmailMessage(boda.EmailMessage, ArrangementObject):
    CONTENT_MODELS = [boda.EmailMessage.EMAIL_MESSAGE_CMODEL,
                      boda.Arrangement.ARRANGEMENT_CONTENT_MODEL]

    NEW_OBJECT_VIEW = 'arrangement:view'

    # messages are related to mailbox via is part of
    mailbox = Relation(relsext.isPartOf, type=Mailbox)

    @property
    def headers(self):
        '''
        Access CERP headers as a dictionary.
        '''
        return dict([(h.name, h.value) for h in self.cerp.content.headers])

    def get_original_datastream(self):
        # for email content, use MIME datastream as original content
        return self.getDatastreamObject('MIME')

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



