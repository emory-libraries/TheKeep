import celery
from django.core.management.base import BaseCommand
from eulfedora.server import Repository

from keep.file.models import DiskImage
from keep.file.tasks import migrate_aff_diskimage


class Command(BaseCommand):
    '''Migrated AFF disk images'''
    help = __doc__

    #: default verbosity level
    v_normal = 1

    def add_arguments(self, parser):
        # Positional arguments: pid
        parser.add_argument('pids', nargs='*',
            help='List of pids to migrate (optional)')


    def handle(self, *args, **kwargs):
        verbosity = kwargs.get('verbosity', self.v_normal)

        # pids specified on command-line take precedence
        pids = kwargs.get('pids', [])
        repo = Repository()
        # if no pids were specified, find all AFFs
        if not pids:
            objs = repo.get_objects_with_cmodel(DiskImage.DISKIMAGE_CONTENT_MODEL,
                type=DiskImage)
            for obj in objs:
                # check premis for to find Disk Images in AFF format;
                # exclude any that have already been migrated
                if obj.provenance.exists:
                    premis = obj.provenance.content
                    if premis.object and premis.object.format \
                                     and premis.object.format.name == 'AFF' \
                                     and not obj.migrated:
                        pids.append(obj.pid)

        # create a celery result set and queue conversion of each pid requested
        # or found in fedora
        migration_tasks = celery.result.ResultSet([])
        for pid in pids:
            migration_tasks.add(migrate_aff_diskimage.delay(pid))

        # wait for tasks to complete
        try:
            migration_tasks.join()
        except Exception:
            # exceptions from tasks gets propagated here, but ignore
            # them and report based on success/failure
            pass

        print '%d migrations completed, %s failures' % \
            (migration_tasks.completed_count(),
            'some' if migration_tasks.failed() else 'no')

        for result in migration_tasks.results:
            if result.state == celery.states.FAILURE:
                print 'Error: %s' % result.result
            else:
                print 'Success: %s' % result.result


