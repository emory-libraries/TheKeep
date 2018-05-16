'''
Manage command to delete duplicate Video objects.
'''
from django.core.management.base import BaseCommand
from eulfedora.server import Repository

from keep.video.models import Video


class Command(BaseCommand):
    '''Find DiskImage objects with content in AD1 format.'''
    help = __doc__

    #: default verbosity level
    v_normal = 1

    def handle(self, *args, **kwargs):
        verbosity = kwargs.get('verbosity', self.v_normal)
        repo = Repository()
        video_duplicates = repo.find_objects(type=Video, label="DELETE")
        for pid in video_duplicates:
            repo.purge_object(pid.pid)