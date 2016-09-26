from django.core.management.base import BaseCommand, CommandError
from eulfedora.server import TypeInferringRepository
from eulfedora.util import RequestFailed
import re
import tempfile


class Command(BaseCommand):
    '''Export an existing Fedora object and import it with a new pid,
preserving all history, datastreams, audit trails, etc.
NOTE: should not be used except in dire need; may not work with large objects.'''
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
        'all': re.compile(r'(?P<digest><foxml:contentDigest[^>]+)DIGEST="[0-9a-f]*"\s*/>')
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

    def handle(self, *args, **options):

        # use type inferring repo so we can set the correct
        # url as the pidman target uri

        repo = TypeInferringRepository()

        for pid in options['pids']:
            # initialize current object so we can determine type,
            # and generate an appropriate Keep url
            obj = repo.get_object(pid)
            # print ds id and checksum (for latest version), to help
            # with verifying content after ingest
            self.datastream_summary(obj)

            # *TEMPORARY* placeholder for new pid
            # TODO: add logic here to find an unused rushdie pid in the
            # rushdie collection allocation (once they are marked) OR
            # mint a new pid.  If using an existing pid, update
            # pid name and target uri based on existing Keep logic.
            newpid = 'newpid:1234'

            # get the archival export of the object from fedora
            response = repo.api.export(obj.pid, context='archive')
            objexport = response.content

            # search and replace within the archive foxml to change
            # every reference from the old pid to the new one
            newpidobj = objexport.replace(obj.pid, newpid)

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
                self.datastream_summary(repo.get_object(newpid))

            except RequestFailed as err:
                print 'Error ingesting %s as %s: %s' % (pid, newpid, err)

            # TODO: leave old version for checking/verification?
            # have an option fo the script to remove automatically?
            # Or maybe the script can verify contents/checksums for
            # unaffected datastreams before purging...

    def datastream_summary(self, obj):
        # print ds id and checksum (for latest version), to help
        # with verifying content after ingest
        for dsid in obj.ds_list.iterkeys():
            # NOTE: could skip DC/RELS-EXT, since wee expect those
            # checksums to change since we have changed the contents
            dsobj = obj.getDatastreamObject(dsid)
            print '%15s %s %s %s' % \
                (dsid, dsobj.checksum_type, dsobj.checksum, dsobj.mimetype)
