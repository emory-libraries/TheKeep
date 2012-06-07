import csv
from collections import defaultdict
from optparse import make_option
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from keep.arrangement.models import ArrangementObject


class Command(BaseCommand):
    help = 'Import verdicts from a CSV file to arrangement objects in the repository'

    option_list = BaseCommand.option_list + (
        make_option('--csv', help='CSV file with verdict information'),
        )

    csv_fields = (
        'id', 'checksum', 'path', 'series', 'subseries', 'verdict',
        'file type', 'file creator', 'attributes', 'created', 'modified',
        'computer', 'size')

    # default django verbosity levels: 0 = none, 1 = normal, 2 = all
    v_normal = 1

    def handle(self, csvfile=None, verbosity=1, *args, **options):
        if csvfile is None:
            raise CommandError('CSV filename is required')

        csvreader = csv.DictReader(open(csvfile, 'rb'),
                                fieldnames=self.csv_fields)
        # skip the header row in CSV file
        csvreader.next()
        verbosity = int(verbosity)

        stats = defaultdict(int)
        for row in csvreader:
            stats['rows'] += 1
            try:
                obj = ArrangementObject.by_arrangement_id(row['id'])
                if verbosity > self.v_normal:
                    print 'Found %s for arrangement id %s' % \
                          (obj.pid, row['id'])
                stats['found'] += 1

            except ObjectDoesNotExist as err:
                stats['not_found'] += 1
                if verbosity >= self.v_normal:
                    print err
            except MultipleObjectsReturned as err:
                stats['too_many'] += 1   
                if verbosity >= self.v_normal:
                    print err


        # summary
        if verbosity >= self.v_normal:
            print '''\nProcessed %(rows)d rows and found %(found)d corresponding record(s)
%(not_found)d record(s) not found, %(too_many)d with multiple matches''' % stats
                    
            


        
