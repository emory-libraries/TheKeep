'''
Manage command to find AD1 disk images.
'''
# from django.template.defaultfilters import filesizeformat, pluralize
from django.core.management.base import BaseCommand
from eulfedora.server import Repository

from keep.file.models import DiskImage


class Command(BaseCommand):
    '''Find DiskImage objects with content in AD1 format.'''
    help = __doc__

    #: default verbosity level
    v_normal = 1

    def handle(self, *args, **kwargs):
        verbosity = kwargs.get('verbosity', self.v_normal)
        repo = Repository()
        objs = repo.get_objects_with_cmodel(DiskImage.DISKIMAGE_CONTENT_MODEL,
            type=DiskImage)
        for obj in objs:
            img_fmt = None

            # use premis object format to distinguish AD1 disk images
            if obj.provenance.exists:
                premis = obj.provenance.content
                if premis.object and premis.object.format:
                    img_fmt = premis.object.format.name

            if img_fmt == 'AD1':
                print obj.pid
            if img_fmt is None and verbosity >= self.v_normal:
                self.stderr.write('Warning: %s has no premis object format' % obj.pid)