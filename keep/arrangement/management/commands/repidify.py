import base64
from collections import OrderedDict
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse
from eulcm.models import boda
from eulfedora.rdfns import relsext
from eulfedora.server import TypeInferringRepository
from eulfedora.util import RequestFailed
from eulxml.xmlmap import mods
import logging
from pidservices.clients import parse_ark
import re
import urllib

from keep.arrangement.models import ArrangementObject, LocalArrangementMods
from keep.common.fedora import ManagementRepository, pidman
from keep.common.utils import absolutize_url


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    '''Export an existing arrangement object and import it with a new pid,
preserving all history, datastreams, audit trails, etc.
NOTE: should not be used except in dire need; may fail on large objects.'''
    help = __doc__

    # regular expressions to remove datastream checksums before reingest
    dsre = {
        # regex to remove datastream version checksum by datastream id
        # for DC and RELS-EXT datastreams affected by pid change
        'dcrels': re.compile(
            r'(?P<dsversion><foxml:datastreamVersion ID="(DC|RELS-EXT).\d+"[^>]*>)\s+' +
            r'<foxml:contentDigest[^>]*DIGEST="[0-9a-f]*"/>',
            flags=re.MULTILINE|re.DOTALL),
        # regex to remove checksums for all xml datastreams,
        # for which Fedora historically has difficulty calculating reliable
        # and repeatable checksums
        'xml': re.compile(
            r'(?P<dsversion><foxml:datastreamVersion[^>]*MIMETYPE="text/xml"[^>]*>)\s+' +
            r'<foxml:contentDigest[^>]*DIGEST="[0-9a-f]*"/>',
            flags=re.MULTILINE|re.DOTALL),
        # regex to remove all datastream checksums, as a fallback for
        # an object that can't be ingested due to checksum errors
        'all': re.compile(r'(?P<digest><foxml:contentDigest[^>]+)DIGEST="[0-9a-f]*"\s*/>'),
        # rels ext base64 encoded ocntent
        'rels_encoded': re.compile(
            r'<foxml:datastreamVersion ID="RELS-EXT.\d+"[^>]*>\s+' +
            r'<foxml:contentDigest[^>]*DIGEST="[0-9a-f]*"/>\s+' +
            r'<foxml:binaryContent>([^<]+)</foxml:binaryContent>',
            flags=re.MULTILINE|re.DOTALL),
    }

    def add_arguments(self, parser):
        parser.add_argument(
            'pids', nargs='+', metavar='PID',
            help='Specify one or more pids for objects to be updated')
        parser.add_argument(
            '--checksum-cleanup', choices=['affected', 'xml', 'all'],
            default='xml',
            help='Datastream checksums to be removed before re-ingest. ' +
                 '(affected: checksums for datastreams affected by pid change; '
                 'default: %(default)s)')
        parser.add_argument(
            '--no-purge', default=False, action='store_true',
            help='Disable automatic purge of old object even if validation ' +
                 'passes.')

    def handle(self, *args, **options):
        if pidman is None:
            raise CommandError("This script requires the PID manager client")

        # use type-inferring repository
        repo = TypeInferringRepository(username=settings.FEDORA_MANAGEMENT_USER,
                                       password=settings.FEDORA_MANAGEMENT_PASSWORD)

        for pid in options['pids']:
            # initialize current object so we can determine type,
            # and generate an appropriate Keep url

            # NOTE: using type inferring repo to get arrangment *or*
            # email content so each type is handled appropriately
            obj = repo.get_object(pid)

            # check that object exists and is an arrangement object
            if not obj.exists:
                self.stderr.write('Error: %s not found' % pid)
                continue

            obj_cmodels = [str(cmodel) for cmodel in obj.get_models()]

            # check by content model instead of class, since could be
            # email content or file content
            if boda.Arrangement.ARRANGEMENT_CONTENT_MODEL not in \
               obj_cmodels:
                self.stderr.write('Error: %s is not an arrangement object' % pid)
                continue

            # explicitly do not convert mailbox objects, since we don't
            # support generating premis for them (no content)
            if boda.Mailbox.MAILBOX_CONTENT_MODEL in obj_cmodels:
                self.stderr.write('Error: mailbox object %s is not supported' % pid)
                continue

            # skip anything without an original datastream (can't generate premis)
            try:
                obj.get_original_datastream()
            except Exception:
                self.stderr.write('Error: %s has no original datastream; not supported' % pid)
                continue

            # set flag so we can check for email messages
            is_email = boda.EmailMessage.EMAIL_MESSAGE_CMODEL in obj_cmodels

            # some email objects don't have a fedora object label, which is
            # used to set the pid name; if email label is empty, use email
            # label method to set it
            if is_email and obj.label is None or obj.label == '':
                obj.label = obj.email_label()

            # todo use pidman client to search for pids in
            # PIDMAN_RUSHDIE_DOMAIN with label PIDMAN_RUSHDIE_UNUSED
            # if none, create a new one; if one is found,
            # update it with object label and target

            # get pid to use for the new object; either unused rushdie
            # pid or a brand new pid; stores ark and ark uri in the metadata
            newpid = self.get_new_pid(obj)

            # get the archival export of the object from fedora
            response = repo.api.export(obj.pid, context='archive')
            objexport = response.content

            # if rels-ext content is base64 encoded, it needs to be
            # decoded first so search and replacing the pid will work

            # search and replace within the archive foxml to change
            # every reference from the old pid to the new one
            newpidobj = objexport.replace(obj.pid, newpid)

            encoded_rels = self.dsre['rels_encoded'].findall(newpidobj)
            for content in encoded_rels:
                # decode the content
                newcontent = base64.b64decode(content)
                # replace old pid with new
                newcontent = newcontent.replace(obj.pid, newpid)
                # replace old encoded cntent with new encoded content
                newpidobj = newpidobj.replace(content, base64.b64encode(newcontent))

            # NOTE: if problems come up with the import foxml,
            # it may be useful to write it out to a tempfile for inspection
            # import tempfile
            # xmlfile = tempfile.NamedTemporaryFile(delete=False)
            # xmlfile.write(newpidobj)
            # xmlfile.close()
            # print 'ingest content : ', xmlfile.name

            # clean up checksums based on requested option
            if options['checksum_cleanup'] == 'all':
                newpidobj = self.dsre['all'].sub(r'', newpidobj)
            else:
                # if either xml or affected datastreams was requested,
                # clean affected datastreams, since rels-ext will not
                # be included by xml regex
                newpidobj = self.dsre['dcrels'].sub(r'\g<dsversion>', newpidobj)

                # if xml checksum removal was requested, run that also
                if options['checksum_cleanup'] == 'xml':
                    newpidobj = self.dsre['xml'] \
                        .sub(r'\g<dsversion>', newpidobj)

            # ingest the new version of the object
            try:
                newpid = repo.ingest(newpidobj)
                print 'Successfully re-ingested %s as %s' % (pid, newpid)
                # init as same type of object as old
                # newobj = repo.get_object(newpid, type=obj.__class__)
                newobj = repo.get_object(newpid)

                # for email objects, update mailbox reference to new pid
                if is_email:
                    # remove relation to old pid
                    obj.mailbox.rels_ext.content.remove(
                        (obj.mailbox.uriref, relsext.hasPart, obj.uriref))
                    # and add relation to the new one
                    obj.mailbox.rels_ext.content.add(
                        (obj.mailbox.uriref, relsext.hasPart, newobj.uriref))
                    obj.mailbox.save('Updating relation for identifier change %s -> %s' % \
                        (obj.noid, newobj.noid))
                    print 'Updated mailbox %s reference for new id %s' % \
                        (obj.mailbox.noid, newobj.noid)

                    # copy updated label if any before checking
                    newobj.label = obj.label

                # store ark and ark uri from in-memory old object before
                # comparing, because comparison seems to replace model-based
                # datastream object types with generic versions

                ark = obj.mods.content.ark
                ark_uri = obj.mods.content.ark_uri

                # validate the new object before purging
                errors = self.compare_objects(obj, newobj)
                # if there are any errors, report and don't purge
                if errors:
                    print 'Error! object validation failed:'
                    for key, val in errors.iteritems():
                        print '%s\t%s' % (key, val)
                else:
                    # purge original unless no purge requested
                    if options['no_purge']:
                        print 'Validation succeeded for %s; not purging %s' % \
                            (newobj.pid, obj.pid)
                    else:
                        purged = repo.purge_object(obj.pid)
                        if purged:
                            print 'Validation succeeded for %s; purged %s' % \
                                (newobj.pid, obj.pid)
                        else:
                            print 'Validation succeeded for %s; error purging %s' % \
                                (newobj.pid, obj.pid)

                # re-init new objet to avoid any weirdness after comparison
                newobj = repo.get_object(newpid)

                # add ark to new object metadata using same logic as at ingest
                # - if we have a mods datastream, store the ARK as mods:identifier
                if hasattr(newobj, 'mods'):
                    # store full uri and short-form ark
                    newobj.mods.content.ark = ark
                    newobj.mods.content.ark_uri = ark_uri
                else:
                    # otherwise, add full uri ARK to dc:identifier
                    newobj.dc.content.identifier_list.append(ark_uri)

                # add premis in order to document the identifier change
                newobj.set_premis_object()
                newobj.identifier_change_event(pid)
                # generated premis should be valid, but double-check before
                # saving invalid premis to fedora
                if not newobj.provenance.content.is_valid():
                    print 'Error! premis is not valid'
                    print newobj.provenance.content.validation_errors()
                else:
                    newobj.save('Add premis with identifier change event; ' +
                                'add ARK to descriptive metadata')

            except RequestFailed as err:
                print 'Error ingesting %s as %s: %s' % (pid, newpid, err)
                raise

    def get_new_pid(self, obj):
        # TODO: first, make sure object label is set appropriately before
        # minting new pid or updating an existing one

        # check to see if there are any unused pids in the rushdie collection
        # that can be re-assigned
        unused_pids = pidman.search_pids(
            domain_uri=settings.PIDMAN_RUSHDIE_DOMAIN,
            target=settings.PIDMAN_RUSHDIE_UNUSED_URI)

        total_found = unused_pids.get('results_count', 0)
        logger.debug('Found %d unused rushdie pids' % total_found)

        # if any unused pids were found, use the first one
        if total_found:
            next_pid = unused_pids['results'][0]
            noid = next_pid['pid']

            print 'Found %d unused rushdie pid%s, using %s' % \
                (total_found, 's' if total_found != 1 else '', noid)

            # update pid metadata to reflect the updated object
            # update the ark name to match the current object
            pidman.update_ark(noid=noid, name=obj.label)
            # update the ark target and ensure it is active

            # generate the keep url for this object, using the same logic
            # in keep.common.fedora for minting new pids
            pid = ':'.join([obj.default_pidspace, noid])
            target = reverse(obj.NEW_OBJECT_VIEW, kwargs={'pid': pid})
            # reverse() encodes the PID_TOKEN and the :, so just unquote the url
            # (shouldn't contain anything else that needs escaping)
            target = urllib.unquote(target)
            # absolutize the url to include configured keep domain
            target = absolutize_url(target)
            # update the existing pid with the new Keep url
            pidman.update_ark_target(noid=noid, target_uri=target, active=True)

            ark_uri = next_pid['targets'][0]['access_uri']
            parsed_ark = parse_ark(ark_uri)
            naan = parsed_ark['naan']  # name authority number
            # short form of ark identifier
            ark = 'ark:/%s/%s' % (naan, noid)

            # NOTE: adding to the old object metadata is semi useless,
            # since the old object will not be saved and the migration,
            # but it provides convenient access to ark and ark_uri

            # store the ark in the object metadata
            # (this logic duplicated from base get_default_pid method)
            # if we have a mods datastream, store the ARK as mods:identifier
            if hasattr(obj, 'mods'):
                # store full uri and short-form ark
                obj.mods.content.identifiers.extend([
                    mods.Identifier(type='ark', text=ark),
                    mods.Identifier(type='uri', text=ark_uri)
                    ])
            else:
                # otherwise, add full uri ARK to dc:identifier
                obj.dc.content.identifier_list.append(ark_uri)

            # return the pid to be used
            return pid

        else:
            # TEST this: can we use default get next pid for arrangement
            # objects (including email)?
            return obj.get_default_pid()
            # this returns the fedora pid, and puts the ark and ark uri
            # in mods or ark uri in dc
            # need to test with normal arrangement objects _and_ email objects

    def compare_objects(self, oldobj, newobj):
        # validate the new version of the object against the old
        # - if a datastream exists in the old object, it should exist
        # in the new object and the checksum should match (with the
        # exception of DC/RELS-EXT, which we expect to be modified due to the
        # text change for the new pid)

        errors = OrderedDict()
        # compare top-level object metadata (except for modified)
        object_properties = ['label', 'owner', 'state', 'created']
        for prop in object_properties:
            if not getattr(oldobj, prop) == getattr(newobj, prop):
                errors[prop] = 'Property mismatch: %s vs %s' % \
                    (getattr(oldobj, prop), getattr(newobj, prop))

        # compare datastreams
        for dsid in oldobj.ds_list.iterkeys():
            old_dsobj = oldobj.getDatastreamObject(dsid)
            old_versions = old_dsobj.history().versions

            # for each version of each datastream, check that the version
            # checksums match or that the same version is present, for dc/rels
            for version in old_versions:
                dsdate = version.created
                old_dsver = oldobj.getDatastreamObject(dsid, as_of_date=dsdate)
                new_dsver = newobj.getDatastreamObject(dsid, as_of_date=dsdate)

                if dsid in ['DC', 'RELS-EXT']:
                    if not new_dsver.exists:
                        errors['%s-%s' % (dsid, dsdate)] = 'missing version'
                else:
                    if not old_dsver.checksum == new_dsver.checksum:
                        errors['%s-%s' % (dsid, dsdate)] = 'checksum mismatch'

        return errors

