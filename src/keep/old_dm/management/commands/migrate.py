import csv
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from keep.old_dm.models import Content, MISSING_COLLECTIONS, ITEMS_WITHOUT_COLLECTION

class Command(BaseCommand):
    '''Migrate metadata for items from the old Digital Masters database into the
    new Repository-based system.
    '''
    help = __doc__

    option_list = BaseCommand.option_list + (
        make_option('--location', '-l',
            dest='location',
            action='store',
            type='string',
            help='''Only include items with the specified Location Name (e.g., MARBL or Emory Archives)'''),
        make_option('--max', '-m',
                    dest='max',
                    action='store',
                    type='int',
                    help='''Stop after processing the specified number of items'''),

        )

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
            # restrict to audio items
            items = Content.audio_objects.all()
            # filter items by location if one was specified
            if 'location' in options and options['location'] is not None:
                items = items.filter(location__name__icontains=options['location'])
            # limit to max number of items if specified
            if 'max' in options:
                items = items[:options['max']]

            for item in items:
                # TODO: make it possible to suppress item info based on verbosity setting
                print 'Item %d' % item.id
                row_data = item.descriptive_metadata()
                row_data += item.source_tech_metadata()
                row_data += item.digital_tech_metadata()
                row_data += item.rights_metadata()
                print '\n'
                csvfile.writerow([_csv_sanitize(field) for field in row_data])


        # TODO: print any filter info (location, max)
        print '\n\n%d audio items (%d total items)' % (items.count(), Content.objects.count())
        
        if MISSING_COLLECTIONS:
            print '\nThe following collections are referenced in the old database but are not yet available in Fedora:'
            for coll, count in MISSING_COLLECTIONS.iteritems():
                print '%s\t\t%d item(s)' % (coll, count)
        if ITEMS_WITHOUT_COLLECTION:
            print '\nThe following %d item(s) do not have a collection specified:' % len(ITEMS_WITHOUT_COLLECTION)
            print ', '.join(['%d' % d for d in ITEMS_WITHOUT_COLLECTION])


# Sanitize field values for use in CSV. The standard csv module in Python
# 2.x accepts only ascii sctrings or utf-8 encodings of unicode strings, so
# encode any unicode strings before passing them into csv.
def _csv_sanitize(value):
    if isinstance(value, unicode):
        return value.encode('utf-8')
    else:
        return value
    
