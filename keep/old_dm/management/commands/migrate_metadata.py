from contextlib import contextmanager
import csv
import logging
from optparse import make_option
import sys

from django.core.management.base import BaseCommand, CommandError

from keep.old_dm.models import Content, MISSING_COLLECTIONS, ITEMS_WITHOUT_COLLECTION

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    '''Migrate metadata for items from the old Digital Masters database into the
    new Repository-based system.
    '''
    help = __doc__

    option_list = BaseCommand.option_list + (
        make_option('--location', '-l',
            help='''Only include items with the specified Location Name (e.g., MARBL or Emory Archives)'''),
        make_option('--max', '-m',
            type='int',
            help='''Stop after processing the specified number of items'''),
        make_option('--csvoutput', '-c',
            help='''Output CSV data to the specified filename'''),
        make_option('--dry-run', '-n',
            default=False,
            action='store_true',
            help='''Report on what would be done, but don't actually migrate anything'''),
        make_option('--dmid', '-i',
            type='int',
            action='append',
	    help='Process a specific item, specified by digital masters id. To process multiple items by id, specify multiple -i options, e.g. -i 11 -i 233'),
        )

    def handle(self, *args, **options):
        # verbosity should be set by django BaseCommand standard options
        verbosity = int(options['verbosity'])    # 1 = normal, 0 = minimal, 2 = all
        v_normal = 1
        if verbosity > v_normal:
            level = logging.DEBUG
        elif verbosity == v_normal:
            level =  logging.INFO
        else:
            level = logging.WARN
        self.config_output(level)

        if options['dry_run']:
            logging.info('Migration dry run. Metadata will be extracted ' +
                         'but not ingested. To ingest metadata, run ' +
                         'without the -n option.')

        with self.open_csv(options) as csvfile:
            if csvfile:
                csvfile.writerow(Content.all_fields)
            # restrict to audio items
            items = Content.audio_objects.all()
            filter_labels = []   # human-readable labels for reporting filters in use
            # filter items by location if one was specified
            if 'location' in options and options['location'] is not None:
                items = items.filter(location__name__icontains=options['location'])
                filter_labels.append("location '%s'" % options['location'])
            if 'dmid' in options and options['dmid']:
                items = items.filter(id__in=options['dmid'])
                filter_labels.append('item id(s) %s' % ', '.join(str(i) for i in options['dmid']))
            # limit to max number of items if specified
            if 'max' in options and options['max']:
                items = items[:options['max']]
                filter_labels.append('maximum %d' % options['max'])

            for item in items:
                logger.info('\nItem %d' % item.id)
                if item.marked_for_deletion():
                    logger.info('DELETE item %d -- Title: %s' % (item.id, item.title))
                    continue

                obj, row_data = item.as_digital_object_and_fields()
                if not options['dry_run']:
                    message = 'Migrated from legacy Digital Masters item %d' % (item.id,)
                    obj.save(logMessage=message)
                    logger.info('Ingested legacy Digital Masters item %d as %s' % (item.id, obj.pid))

#                    title_prefix = '(migrated to The Keep: %s) ' % (obj.pid,)
#                    item.title = title_prefix + item.title
#                    item.save()
                if csvfile:
                    csvfile.writerow([_csv_sanitize(field) for field in row_data])


        filter = ''
        if filter_labels:
            filter = 'with %s' % ', '.join(filter_labels)
        logger.info('\n\n%d audio items %s (%d total items)' % (items.count(), filter, Content.objects.count()))
        
        if MISSING_COLLECTIONS:
            warning = '\nThe following collections are referenced in the old database but are not yet available in Fedora:\n'
            warning += '\n'.join('%s\t\t%d item(s)' % (coll, count) for coll, count in MISSING_COLLECTIONS.iteritems())
            logger.warn(warning)
            
        if ITEMS_WITHOUT_COLLECTION:
            warning =  '\nThe following %d item(s) do not have a collection specified:\n' % len\
                (ITEMS_WITHOUT_COLLECTION)
            warning += ', '.join('%d' % d for d in sorted(ITEMS_WITHOUT_COLLECTION))
            logger.warn(warning)

    @contextmanager
    def open_csv(self, options):
        if options['csvoutput']:
            with open(options['csvoutput'], 'wb') as f:
                csvfile = csv.writer(f)
                yield csvfile
        else:
            yield None


    def config_output(self, level):
        # configure logger to be used for script output
        logger = logging.getLogger('keep.old_dm')
        logger.setLevel(level)
        # customize log output slightly
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        # use custom simple formatter
        ch.setFormatter(SimpleFormatter())
        logger.addHandler(ch)
        # don't propagate to root logger
        logger.propagate = False


# Sanitize field values for use in CSV. The standard csv module in Python
# 2.x accepts only ascii sctrings or utf-8 encodings of unicode strings, so
# encode any unicode strings before passing them into csv.
def _csv_sanitize(value):
    if isinstance(value, unicode):
        return value.encode('utf-8')
    else:
        return value

class SimpleFormatter(logging.Formatter):
    # simple log formatter - generally only displays the log message, but for single-line messages with a log level
    # greater than logging.INFO, pre-pends the level name to the beginning of the message.
    def __init__(self, fmt='%(message)s', datefmt=None):
        logging.Formatter.__init__(self, fmt=fmt, datefmt=datefmt)

    def format(self, record):
        text = logging.Formatter.format(self, record)
        if record.levelno > logging.INFO and '\n' not in text:
            text = '%s: %s' % (record.__dict__['levelname'], text)
        return text
