import csv

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

        with open('migrate.csv', 'wb') as f:           # TODO: make filename configurable
            csvfile = csv.writer(f)
            csvfile.writerow(Content.all_fields)

            for item in Content.audio_objects.all():
                # TODO: make it possible to suppress item info based on verbosity setting
                print 'Item %d' % item.id
                row_data = item.descriptive_metadata()
                row_data += item.source_tech_metadata()
                print '\n'
                csvfile.writerow(_csv_sanitize(field) for field in row_data)


        print '\n\n%d audio items (%d total items)' % (Content.audio_objects.count(), Content.objects.count())


# Sanitize field values for use in CSV. The standard csv module in Python
# 2.x accepts only ascii sctrings or utf-8 encodings of unicode strings, so
# encode any unicode strings before passing them into csv.
def _csv_sanitize(value):
    if isinstance(value, unicode):
        return value.encode('utf-8')
    else:
        return value
    
