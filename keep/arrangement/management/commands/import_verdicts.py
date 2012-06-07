import csv
from collections import defaultdict
from optparse import make_option
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from eulfedora.util import RequestFailed

from keep.arrangement.models import ArrangementObject
from keep.common.models import rights_access_terms_dict

class Command(BaseCommand):
    help = 'Import verdicts from a CSV file to arrangement objects in the repository'
    args = '--csv <csvfile>'
    option_list = BaseCommand.option_list + (
        make_option('--csv', dest='csvfile',
                    help='CSV file with verdict information (REQUIRED)'),
        make_option('-n', '--noact', action='store_true', default=False,
                    help='''Test run: report what would be done, but do not modify
                    anything in the repository'''),
        )

    # expected columns in the csv file
    csv_fields = (
        'id', 'checksum', 'path', 'series', 'subseries', 'verdict',
        'file type', 'file creator', 'attributes', 'created', 'modified',
        'computer', 'size')

    # map text verdicts from csv file to rights access code
    csv_verdict = {
        'As Is': '2',
        'Restricted': '4',
        'Virtual': '2'
    }

    # default django verbosity levels: 0 = none, 1 = normal, 2 = all
    v_normal = 1

    def handle(self, csvfile=None, verbosity=1, noact=False, *args, **options):
        if csvfile is None:
            raise CommandError('CSV filename is required')
        verbosity = int(verbosity)  # ensure we compare int to int


        csvreader = csv.DictReader(open(csvfile, 'rb'),
                                fieldnames=self.csv_fields)
        # skip header row
        csvreader.next()

        stats = defaultdict(int)
        verdict_stats = defaultdict(int)
        for row in csvreader:
            stats['rows'] += 1
            try:
                obj = ArrangementObject.by_arrangement_id(row['id'])
                if verbosity > self.v_normal:
                    print 'Found %s for arrangement id %s' % \
                          (obj.pid, row['id'])
                    
                stats['found'] += 1

                # set rights status based on verdict in csv

                # TODO: what are we doing with missing/empty verdict ? 
                
                if not row['verdict']:
                    if verbosity >= self.v_normal:
                        print 'No verdict set for %(id)s' % row
                    continue
                
                verdict = row['verdict'].strip()
                if verdict not in self.csv_verdict:
                    if verbosity >= self.v_normal:
                        print 'Verdict "%(verdict)s" not recognized (%(id)s)' % row
                    continue
                else:
                    # set code & text based on verdict in CSV

                    # TODO: for email, we will need to handle numeric code
                    
                    access_code = self.csv_verdict[verdict]

                    # report previous status in case we're changing a previously
                    # assigned verdict
                    if verbosity >= self.v_normal and obj.rights.exists \
                       and obj.rights.content.access_status and \
                       obj.rights.content.access_status.code != access_code:
                        
                        # 5300c imported as 10/undetermined; only report 10
                        # in full verbose mode
                        if obj.rights.content.access_status.code != '10' or \
                           verbosity > self.v_normal:
                            print 'Previous access code for %s was %s; changing to %s' % \
                                  (row['id'], obj.rights.content.access_status.code,
                                   access_code)

                    # set rights code & text based on verdict
                    obj.rights.content.create_access_status()
                    obj.rights.content.access_status.code = access_code 
                    obj.rights.content.access_status.text = rights_access_terms_dict[access_code].text

                    # if not noact mode, save object
                    if not noact:
                        try:
                            # only save if changed, so we can keep track of
                            # how many updates are made
                            if obj.rights.isModified():  
                                updated = obj.save('import verdict')
                                stats['updated'] += 1
                                
                        except RequestFailed:
                            print 'Error saving %s' % obj.pid
                            stats['save_error'] += 1
                    
                    # update tally for this verdict
                    verdict_stats[verdict] += 1

            except ObjectDoesNotExist as err:
                stats['not_found'] += 1
                if verbosity >= self.v_normal:
                    print 'Error: %s' % err
            except MultipleObjectsReturned as err:
                stats['too_many'] += 1   
                if verbosity >= self.v_normal:
                    print 'Error: %s' % err


        # summary
        if verbosity >= self.v_normal:
            print '''\nProcessed %(rows)d rows and found %(found)d corresponding record(s)
%(not_found)d record(s) not found, %(too_many)d with multiple matches''' % stats
            print 'Verdicts imported:\n    ' + \
                  '; '.join('%d %s' % (n, v) for v, n in verdict_stats.iteritems())
            if not noact:
                print 'Updated %(updated)d record(s); error saving %(save_error)d records' \
                      % stats
                    
            


        
