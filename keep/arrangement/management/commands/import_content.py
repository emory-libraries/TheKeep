import csv
from collections import defaultdict
import magic
from optparse import make_option
import os.path
from django.core.management.base import BaseCommand, CommandError
from eulfedora.rdfns import relsext, model as modelns
from eulfedora.util import RequestFailed
from eulcm.models.boda import RushdieFile
from rdflib import URIRef

from keep.arrangement.models import ArrangementObject
from keep.collection.models import SimpleCollection as ProcessingBatch
from keep.common.fedora import Repository
from keep.common.utils import md5sum 

class Command(BaseCommand):
    help = '''Import content from a mounted disk image to arrangement objects in the
repository (one-time import for 5300c content)'''
    args = '<mounted disk image path> <batch id>'
    option_list = BaseCommand.option_list + (
        make_option('-n', '--noact', action='store_true', default=False,
                    help='''Test run: report what would be done, but do not modify
                    anything in the repository'''),
        )
    # default django verbosity levels: 0 = none, 1 = normal, 2 = all
    v_normal = 1


    def handle(self, base_path=None, batch_id=None, verbosity=1, noact=False, *args, **options):
        # check path
        if base_path is None:
            raise CommandError('Disk image base path is required')
        if not os.path.isdir(base_path):
            raise CommandError('Disk image base path is not a directory')

        # check batch object
        if batch_id is None:
            raise CommandError('Processing batch id is required')
        self.verbosity = int(verbosity)  # ensure we compare int to int
        
        repo = Repository()
        batch = repo.get_object(batch_id, type=ProcessingBatch)
        if not batch.exists:
            raise CommandError('Processing batch %s not found' % batch_id)
        print 'Importing original content for items in processing batch "%s"' % batch.label

        # iterate over all items that are part of this batch
        items = list(batch.rels_ext.content.objects(batch.uriref, relsext.hasMember))

        mimemagic = magic.Magic(mime=True)

        for i in items:
            # for now, init as file objects since we expect to add original file content
            # (still has arrangement metadata + filetech)
            # TODO: handle special file types, e.g. email
            obj = repo.get_object(str(i), type=RushdieFile)
            # NOTE: in dev/test, collection currently references all items
            # but only a handful actually exist in dev/test repo; just skip 
            if not obj.exists:
                continue
            
            print '%s %s' % (obj.pid, obj.label)
            if obj.original.exists:
                print '%s already has original datastream; skipping' % obj.pid
                continue
                
            if not obj.filetech.exists:
                print 'Error: no file tech (path info) for %s; skipping' % obj.pid
                continue
                
            local_path = None
            filetech_md5 = None
            # There could potentially be multiple file paths; find
            # the one for this computer.
            for f in obj.filetech.content.file:
                if f.computer == batch.label:
                    local_path = f.path
                    filetech_md5 = f.md5
                    break

            # if no path was found, report and skip
            if local_path is None:
                print 'Failed to find local path for %s for computer %s' % \
                      (obj.pid, batch.label)
                continue
            

            # path to grab the original file
            # stored path is absolute; we need it relative to base path
            mac_hd_path = '/Macintosh HD/'
            if local_path.startswith(mac_hd_path):
                local_path = local_path[len(mac_hd_path):]
            disk_path = os.path.join(base_path, local_path)
            if not os.path.isfile(disk_path):
                print 'Computed disk image path %s is not a file' % disk_path
                continue
            
            local_md5 = md5sum(disk_path)
            if filetech_md5 is not None and local_md5 != filetech_md5:
                print 'Local MD5 checksum (%s) does not match checksum in filetech (%s)' \
                      % (local_md5, filetech_md5)
                # stop processing this record
                continue
            if filetech_md5 is None:
                print 'Warning: no MD5 currently stored for %s' % obj.pid
            # TODO: if filetech_md5 (for this computer) is None, we need to set it
            # (other info also ?)
            

            mimetype = mimemagic.from_file(disk_path)
            with open(disk_path) as original_file:
                obj.original.content = original_file
                obj.original.checksum = local_md5
                obj.original.mimetype = mimetype

                # add rushdie-file content model if not already present
                if not obj.has_requisite_content_models:
                    obj.rels_ext.content.add((obj.uriref, modelns.hasModel,
                                       URIRef(RushdieFile.RUSHDIE_FILE_CMODEL)))
                    
                if not noact:
                    # TODO: try/catch, reporting/stats
                    obj.save('adding original file content from disk image')
                
            
