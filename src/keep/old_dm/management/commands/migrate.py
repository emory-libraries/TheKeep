from django.core.management.base import BaseCommand, CommandError

from keep.old_dm.models import Content

class Command(BaseCommand):
    '''Migrate metadata for items from the old Digital Masters database into the
    new Repository-based system.
    '''
    help = __doc__

#    option_list = BaseCommand.option_list + (
#        make_option('--dry-run', '-n',
#            dest='dryrun',
#            action='store_true',
#            help='''Report on what would be done, but don't actually migrate anything'''),
#        )

    def handle(self, *args, **options):
        # verbosity should be set by django BaseCommand standard options
        #verbosity = int(options['verbosity'])    # 1 = normal, 0 = minimal, 2 = all
        #v_normal = 1

        for item in Content.audio_objects.all():
            print 'Item %d' % item.id
            item.descriptive_metadata()
            print '\n'


        print '\n\n%d audio items (%d total items)' % (Content.audio_objects.count(), Content.objects.count())
