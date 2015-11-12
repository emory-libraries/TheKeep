'''
Manage command to ingest migration disk images and associate them
with the existing disk image object they replace.
'''
from django.core.management.base import BaseCommand
from eulfedora.server import Repository
import glob
import os

from keep.file.models import DiskImage


class Command(BaseCommand):
    '''Ingest migrated disk images and associate with older disk images.'''
    help = __doc__

    #: default verbosity level
    v_normal = 1

    def add_arguments(self, parser):
        # Positional arguments: required directory to pick up content
        parser.add_argument('directory',
            help='Path to directory containing bags with disk images')
        parser.add_argument('--pidspace', default='emory',
            help='Fedora pidspace to use when looking for original (default: %(default)s')


    def handle(self, *args, **kwargs):
        verbosity = kwargs.get('verbosity', self.v_normal)
        repo = Repository()

        bags = glob.glob('%s/*/bagit.txt' % kwargs['directory'].rstrip('/'))
        if not bags:
            self.stderr.write('No bagit content found to migrate')
            return

        for bagname in bags:
            bagpath = os.path.dirname(bagname)
            # for now, assuming bagit name is noid portion of object pid
            noid = os.path.basename(bagpath)
            # find the original that this is a migration of
            original = repo.get_object('%s:%s' % (kwargs['pidspace'], noid),
                type=DiskImage)
            # make sure object exists and is a disk image
            if not original.exists:
                print '%s not found in Fedora' % original.pid
                continue
            elif not original.has_requisite_content_models:
                print '%s is not a disk image; skipping' % original.pid
                continue
            # TODO: check if original already has a migration?

            # create a new "migrated" disk image object from the bag
            # for now, assuming we should not use file uri
            # TODO: make this configurable via command-line option?
            migrated = DiskImage.init_from_bagit(bagpath, file_uri=False)
            # associate with original
            migrated.original = original
            # copy over descriptive & rights metadata
            # - collection membership
            migrated.collection = original.collection
            # - mods title, covering dates, abstract
            migrated.mods.content.title = original.mods.content.title
            migrated.mods.content.abstract = original.mods.content.abstract
            migrated.mods.content.coveringdate_start = original.mods.content.coveringdate_start
            migrated.mods.content.coveringdate_end = original.mods.content.coveringdate_end
            # - entire rights datastream
            migrated.rights.content = original.rights.content

            # TODO: insert premis migration event, referencing original


            migrated.save('Ingest migrated version of %s' % original.pid)
            print 'migrated object ingested as %s' % migrated.pid

            # update original object
            original.migrated = migrated.pid
            # TODO: insert deletion premis event for original
            original.save()
