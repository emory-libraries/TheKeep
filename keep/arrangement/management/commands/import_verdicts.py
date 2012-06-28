import csv
from collections import defaultdict
from optparse import make_option
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from eulfedora.util import RequestFailed

from keep.arrangement.models import ArrangementObject, EmailMessage
from keep.common.models import rights_access_terms_dict
from keep.common.eadmap import Series
from keep.common.utils import solr_interface

class Command(BaseCommand):
    help = 'Import verdicts from a CSV file to arrangement objects in the repository'
    args = '--csv <csvfile>'
    option_list = BaseCommand.option_list + (
        make_option('--csv', dest='csvfile',
                    help='CSV file with verdict information (REQUIRED)'),
        make_option('--email', dest='email',
                    action='store_true', default=False,
                    help='Use this option when processing CSV with verdicts for emails'),
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
        'Virtual': '2',
        'needs-review' : '4',
        'family-corr' : '4',
        'rushdie-restrict' : '4',
        'restricted-marbl' : '4',
        'rushdie-approve': '2',
        'in': '2',
        'out': '2',
        'old-in': '2',
        'old-out': '2'
    }

    # default django verbosity levels: 0 = none, 1 = normal, 2 = all
    v_normal = 1

    rushdie_ead_ark = 'http://pid.emory.edu/ark:/25593/8zv36'
    rushdie_eadid = 'rushdie1000'
    rushdie_ead_baseurl = 'https://findingaids.library.emory.edu/documents/rushdie1000/'

    def handle(self, csvfile=None, verbosity=1, noact=False, email=False, *args, **options):
        if csvfile is None:
            raise CommandError('CSV filename is required')
        self.verbosity = int(verbosity)  # ensure we compare int to int

        # load findingaid series/subseries info
        self.load_series_subseries()

        csvreader = csv.DictReader(open(csvfile, 'rb'),
                                fieldnames=self.csv_fields)
        # skip header row
        csvreader.next()

        self.stats = defaultdict(int)
        self.verdict_stats = defaultdict(int)
        series_stats = defaultdict(int)
        for row in csvreader:
            self.stats['rows'] += 1
            try:
                # if email flag then only run logic for email objects
                if email:
                    if not row['checksum']:
                        print "Row Missing checksum"
                        continue
                    else:
                        checksum = row['checksum']
                    if not row['path']:
                        print "Row Missing path"
                        continue
                    else:
                        path = row['path']

                    self.procss_email(checksum, path, noact)
                else:
                    # check if there is a duplicate checksum
                    if row['checksum']:
                        solr = solr_interface()
                        q = solr.query(content_md5=row['checksum'],
                                       content_model=ArrangementObject.ARRANGEMENT_CONTENT_MODEL) \
                                       .field_limit(['pid', 'title', 'simpleCollection_label'])
                        num_found = len(q)
                        if num_found > 1:
                            print 'Error: found more than one record with matching checksum for %s:' \
                                  % row['id']

                            for record in q:
                                # simple collection field is multiple, even though
                                # our content currently only belongs to one;
                                # join into a single field that can be used for output
                                record['collection']  = ', '.join(record['simpleCollection_label'])
                                print '  %(pid)s - %(title)s (%(collection)s)' % record

                            # skip this record, must be handled manually
                            continue

                        # if there is exactly one match, save it to confirm with
                        # pid found by arrangement id
                        elif num_found == 1:
                            checksum_pid = q[0]['pid']



                    obj = ArrangementObject.by_arrangement_id(row['id'])
                    if self.verbosity > self.v_normal:
                        print 'Found %s for arrangement id %s' % \
                              (obj.pid, row['id'])

                    if obj.pid != checksum_pid:
                        print 'Error: pid found by checksum (%s) does not match pid found by arrangement id (%s)' \
                              % (checksum_pid, obj.pid)

                        continue




                    self.stats['found'] += 1

                    # set rights status based on verdict in csv

                    # if no verdict is set, default to restricted
                    if not row['verdict']:
                        row['verdict'] = 'Restricted'
                        if self.verbosity >= self.v_normal:
                            print 'No verdict set for %(id)s; defaulting to restricted' % row


                    # set access code,
                    verdict_assigned = self.set_access_status(obj,
                                                              row['verdict'], row)
                    if verdict_assigned:
                        # update tally for this verdict if successful
                        self.verdict_stats[verdict_assigned] += 1

                    # set series/subseries information
                    series = self.set_series(obj, row)
                    if series:
                        series_stats[series] += 1

                    # if not noact mode, save object
                    if not noact:
                        try:
                            # only save if changed, so we can keep track of
                            # how many updates are made
                            if obj.rights.isModified() or obj.mods.isModified():
                                updated = obj.save('import verdict & series/subseries')
                                self.stats['updated'] += 1

                        except RequestFailed:
                            print 'Error saving %s' % obj.pid
                            self.stats['save_error'] += 1


            except ObjectDoesNotExist as err:
                self.stats['not_found'] +=1
                if self.verbosity >= self.v_normal:
                    print 'Error: %s' % err
            except MultipleObjectsReturned as err:
                self.stats['too_many'] += 1
                if self.verbosity >= self.v_normal:
                    print 'Error: %s' % err


        # summary
        if self.verbosity >= self.v_normal:
            print '''\nProcessed %(rows)d rows and found %(found)d corresponding record(s)
%(not_found)d record(s) not found, %(too_many)d with multiple matches''' % self.stats
            print 'Verdicts imported:\n    ' + \
                  '; '.join('%d %s' % (n, v)
                            for v, n in self.verdict_stats.iteritems())
            print 'Series and subseries assigned:\n  '+ \
                  '\n  '.join('%s : %d' % (v, n)
                            for v, n in series_stats.iteritems())
            if not noact:
                print 'Updated %(updated)d record(s); error saving %(save_error)d records' \
                      % self.stats
                    
            

    def set_access_status(self, obj, verdict, data):
        '''
        Set the access status code on an object based on a text
        verdict string from a CSV file

        :returns: False for an unrecognized verdict; normalized
            verdict string for successful update.
        '''
        
        verdict = verdict.strip()
        if verdict not in self.csv_verdict:
            if self.verbosity >= self.v_normal:
                print 'Verdict "%(verdict)s" not recognized (%(id)s)' % data
                
            # stop processing
            return False

    
        # set code & text based on verdict in CSV

        # TODO: for email, we will need to handle numeric code
        access_code = self.csv_verdict[verdict]

        # report previous status in case we're changing a previously
        # assigned verdict
        if self.verbosity >= self.v_normal and obj.rights.exists \
               and obj.rights.content.access_status and \
            obj.rights.content.access_status.code != access_code:
        
            # 5300c imported as 10/undetermined; only report 10
            # in full verbose mode
            if obj.rights.content.access_status.code != '10' or \
                   self.verbosity > self.v_normal:
                print 'Previous access code for %s was %s; changing to %s' % \
                      (data['id'], obj.rights.content.access_status.code,
                       access_code)

        # set rights code & text based on verdict
        obj.rights.content.create_access_status()
        obj.rights.content.access_status.code = access_code 
        obj.rights.content.access_status.text = rights_access_terms_dict[access_code].text
        
        return verdict

        
    def load_series_subseries(self):
        # load series/subseries deails to map csv series names

        # query the rushdie findingaid for series/subseries info
        series = Series.objects.filter(eadid=self.rushdie_eadid)\
                 	.only('id', 'did__unittitle', 'subseries', 'eadid')

        # create dictionaries to look up values
        by_id = {}  # full details by id
        by_name = {} # name -> id to map from csv file
        for s in series:
            by_id[s.id] = {'title': s.title, 'short_id': s.short_id}
            by_name[s.title] = s.id
            #print 'title = %s id = %s' % (s.title, s.id)
            for sub in s.subseries:
                #print 'title = %s id = %s' % (sub.title, sub.id)
                by_id[sub.id] = {'title': sub.title, 'short_id': sub.short_id,
                                'series': s.id}
                by_name[sub.title] = sub.id

        self.series_by_id = by_id
        self.series_by_name = by_name


    def set_series(self, obj, info):
        '''
        Update series and subseries for an object based on a text
        series names from CSV file data.

        :returns: False if series is not recognized; returns a
            normalized version with the series and subseries applied
            for a successful update.
        '''

        # convert text series/subseries rom CSV to mods
        series = info['series'].strip()
        # TODO: check that this conversion is correct 
        if series == 'Writings':
            series = 'Writings by Rushdie'
        subseries = info['subseries'].strip()

        # check if either series or subseries can't be mapped
        # -- if set but not recognized , bail out
        if series not in self.series_by_name:
            if self.verbosity >= self.v_normal:
                print 'Series "%(series)s" not recognized (%(id)s)' \
                      % info
                return False
            
        if subseries and subseries not in self.series_by_name:
            if self.verbosity >= self.v_normal:
                print 'Subseries "%(subseries)s" not recognized (%(id)s)' \
                      % info
            return False

        # set series details in mods
                    
        # NOTE: exact structure is undocumented and probably not what
        # we really want in the long-term; trying to keep consistent
        # with current ocntent for now...

        # store previous series/subseries value (if set), to report if
        # there is a change
        prev_series = None
        if obj.mods.content.series and obj.mods.content.series.title:
            if obj.mods.content.series.series and \
                   obj.mods.content.series.series.title:
                prev_series = '%s > %s' % \
                              (obj.mods.content.series.series.title,
                               obj.mods.content.series.title)
            else:
                prev_series = obj.mods.content.series.title

        obj.mods.content.create_series()
        if subseries:
            # If there is a subseries, set series info as
            # mods.content.series.series 
            obj.mods.content.series.create_series()
            self.set_series_info(obj.mods.content.series.series,
                                 series)
        else:
            # If there is a series and no subseries, set series info
            # as mods.content.series 
            self.set_series_info(obj.mods.content.series,
                                 series)

        # if there is a subseries, set it
        if subseries:
            self.set_series_info(obj.mods.content.series, subseries)

            new_series = '%s > %s' % (series, subseries)

        else:
            new_series = series

        # if there was a previous value different from the new one,
        # report both new and old series/subseries
        if prev_series is not None and prev_series != new_series \
               and self.verbosity >= self.v_normal:
            print 'Previous series for %s was %s; now %s' % \
                  (obj.pid, prev_series, new_series)

        return new_series


    def set_series_info(self, mods_series, series):
        '''
        Given a mods series object and a series name, look up series
        information and set series details in the mods object.
        '''
        series_id = self.series_by_name[series]
        series_info = self.series_by_id[series_id]        
        mods_series.title = series_info['title']
        mods_series.full_id = series_id
        mods_series.short_id = series_info['short_id']
        mods_series.base_ark = self.rushdie_ead_ark
        # construct url to this series or subseries
        url_parts = [self.rushdie_ead_baseurl]
        # if this is subseries, parent series id goes first
        if 'series' in series_info and series_info['series']: 
            url_parts.append(self.series_by_id[series_info['series']]['short_id'])
        url_parts.append(series_info['short_id'])
        mods_series.uri = '/'.join(url_parts)

    def procss_email(self, checksum, path, noact):
        '''Process verdicts for email content.

        :param checksum: checksum from the CSV file to search on

        :param path: folder/subject of the email message.
        This is used to determine verdict

        :param noact: specifies noact mode

        '''
        obj = EmailMessage.by_checksum(checksum)
        self.stats['found'] += 1

        verdict = path.split('/')[0]
        verdict_assigned = self.set_access_status(obj, verdict, {'verdict': verdict, 'id': checksum})
        self.verdict_stats[verdict_assigned] += 1

        if not noact:
            try:
                # only save if changed, so we can keep track of
                # how many updates are made
                if obj.rights.isModified() or obj.mods.isModified():
                    updated = obj.save('import verdict & series/subseries')
                    self.stats['updated'] += 1

            except RequestFailed:
                print 'Error saving %s' % obj.pid
                self.stats['save_error'] += 1

            print 'Updated %(updated)d record(s); error saving %(save_error)d records' \
                      % self.stats
