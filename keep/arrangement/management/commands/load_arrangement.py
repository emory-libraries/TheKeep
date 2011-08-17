import csv
from optparse import make_option

from eulfedora.rdfns import relsext as relsextns

from django.core.management.base import BaseCommand, CommandError

from keep.arrangement.models import ArrangementObject
from keep.collection.models import CollectionObject, SimpleCollection
from keep.common.eadmap import Series
from keep.common.fedora import Repository

#REMOVE THIS
import pprint

class Command(BaseCommand):
    '''Read CSV file and creates (or adds to) a Simple Collection and associated ArrangementObjects
    with the SimpleCollection and the Master collection'''

    #Set up additional options
    option_list = BaseCommand.option_list + (
        make_option('--noact', '-n',
            action='store_true',
            dest='no-act',
            default=False,
            help='Does not create PIDs or ingest anything into Fedora. Only parses file and outputs results'),
        make_option('--add', '-a',
            action='store',
            dest='add',
            help='adds to the SimpleCollection specified by pid, does not create a new SimpleCollection'),
    )

    args = '<CSV file> <master collection pid> <new simple collection name>'
    help = __doc__

    def _create_series_lookup(self):
        #series / subseries info
        self.series = {}

        #exist query params
        return_fields = ['eadid']
        search_fields = {'eadid' : 'rushdie1000'}

        queryset = Series.objects.also(*return_fields).filter(**search_fields)
        for s in queryset:
            #series info
            self.series[s.title]= {}
            self.series[s.title]['series_info'] = {}
            self.series[s.title]['series_info']['id'] = s.id
            self.series[s.title]['series_info']['short_id'] = s.short_id
            self.series[s.title]['series_info']['base_ark'] = s.eadid.url
            self.series[s.title]['series_info']['uri'] = "https://findingaids.library.emory.edu/documents/%s/%s" % \
                (s.eadid.value, s.short_id)
            #subseries info
            if s.subseries:
                self.series[s.title]['subseries_info'] = {}
                for sub in s.subseries:
                    self.series[s.title]['subseries_info'][sub.title] = {}
                    self.series[s.title]['subseries_info'][sub.title]['id'] = sub.id
                    self.series[s.title]['subseries_info'][sub.title]['short_id'] = sub.short_id
                    self.series[s.title]['subseries_info'][sub.title]['base_ark'] = s.eadid.url
                    self.series[s.title]['subseries_info'][sub.title]['uri'] = "https://findingaids.library.emory.edu/documents/%s/%s/%s" % \
                    (s.eadid.value, s.short_id, sub.short_id)

        #REMOVE 2 lines
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.series)

#    def _get_mods_values(self):
#        return {}



    def _create_arrangement(self, row):
        # set values in filetech DS
        obj = self.repo.get_object(type=ArrangementObject)
        obj.label = row['filename']
        obj.filetech.content.local_id = row['id']
        obj.filetech.content.md5 = row['checksum']
        obj.filetech.content.computer = row['computer']
        obj.filetech.content.path = row['filename']
        obj.filetech.content.attributes = row['attrib']
        obj.filetech.content.created = row['created']
        obj.filetech.content.modified = row['modified']
        obj.filetech.content.type = row['rec_type']
        obj.filetech.content.creator = row['creator']

#        # set values in mods DS
#        mods_values = _get_mods_values(self)
#        #map subseries which is the outer series first
#        obj.mods.content.series.title = mods_values['ss_title']
#        obj.mods.content.series.uri = mods_values['ss_uri']
#        obj.mods.content.series.base_ark = mods_values['ss_base_ark']
#        obj.mods.content.series.full_id = mods_values['ss_full_id']
#        obj.mods.content.series.short_id = mods_values['ss_short_id']
#         #map series which is the inner series
#        obj.mods.content.series.series.title = mods_values['s_title']
#        obj.mods.content.series.series.uri = mods_value['s_uri']
#        obj.mods.content.series.series.base_ark = mods_values['s_base_ark']
#        obj.mods.content.series.series.full_id = mods_values['s_full_id']
#        obj.mods.content.series.series.short_id = mods_values['s_short_id']


        # set association to master collection
        relation = (obj.uriref, relsextns.isMemberOf, self.master_obj.uriref)
        obj.rels_ext.content.add(relation)
        if self.verbosity > self.v_normal:
            self.stdout.write("Adding %s isMemberOf %s relation on ArrangementObject\n" % (obj.label, self.master_obj.pid))

        return obj



    def handle(self, *args, **options):
        #collect arrangement pids here to delete later if SimpleCollection fails to save
        self.arrangement_pids = []
#        self._create_series_lookup()
#        exit()
        
        #0 = none, 1 = normal, 2 = all
        self.v_none = 0
        self.v_normal = 1

        if 'verbosity' in options:
            self.verbosity = int(options['verbosity'])
        else:
            self.verbosity = self.v_normal
        #Create the repo
        self.repo = Repository()

        #Check to make sure all args and options are present
        try:
            file =  args[0]
        except IndexError:
            raise CommandError("No CSV file specified")

        try:
            self.master_pid =  args[1]
        except IndexError:
            raise CommandError("No master collection pid specified")

        #if -a or --add is used the new SimpleCollection name is ignored
        try:
            if not options["add"]:
                self.simple_collection_name =  args[2]
            else:
                self.simple_collection_pid = options["add"]

        except IndexError:
            raise CommandError("An existing SimpleCollection pid must be specified with the -a option or \
            a new SimpleCollection name must be specified as an argument")

        #If Master collection does not exist then raise an exception
        self.master_obj = self.repo.get_object(type = CollectionObject, pid=self.master_pid)

        if not self.master_obj.exists:
            raise CommandError("Master Collection %s does not exist" % (self.master_pid))
        else:
            if self.verbosity > self.v_none:
                self.stdout.write("Using Master Collection: %s(%s)\n" % (self.master_obj.label, self.master_obj.pid))

        #Get or create SimpleColletion object
        #TODO Not sure why I have to do a try block to prevent a 404 here when I don't in other places
        try:
            if options["add"]:
                simple_collection = self.repo.get_object(type=SimpleCollection, pid=self.simple_collection_pid)
            else:
                simple_collection = self.repo.get_object(type=SimpleCollection)
                simple_collection.label = self.simple_collection_name
        except:
            raise CommandError("Pid %s does not exist" % self.simple_collection_pid)

        #try to read file into a dict and assign the field names
        try:
            reader = csv.DictReader(open(file, 'rb'),
                                    fieldnames=["id","checksum","filename","rec_type","file_type",
                                                "creator","attrib","created","modified","computer","size"])
            if self.verbosity > self.v_none:
                self.stdout.write("Reading CSV: %s\n" % (file))
        except IOError:
            raise CommandError("Could not read file %s" % file)


        # skip the header row in CSV file
        reader.next()
        
        #read each field
        csv_read = 0
        arrangement_saved =0
        errors = 0
        for row in reader:
            csv_read += 1
            arrangement_object = self._create_arrangement(row)

            if not options['no-act']:
                try:
                    arrangement_object.save()
                    arrangement_saved += 1
                    self.arrangement_pids.append(arrangement_object.pid)
                    if self.verbosity > self.v_none:
                        self.stdout.write("Saved ArrangementObject %s(%s)\n" % (arrangement_object.label, arrangement_object.pid))
                except Exception as e:
                    if self.verbosity > self.v_none:
                        self.stdout.write("Error saving ArrangementObject %s: %s\n" % (arrangement_object.label, e.message))
                    errors += 1


            if self.verbosity > self.v_normal:
                self.stdout.write("===RELS-EXT===\n")
                for entry in arrangement_object.rels_ext.content:
                    self.stdout.write("%s" % list(entry))
            elif self.verbosity > self.v_none:
                self.stdout.write("TEST ArrangementObject %s\n" % (arrangement_object.label))

            #Add each ArrangementObject to the SimpleCollection
            relation = (simple_collection.uriref, relsextns.hasMember, arrangement_object.uriref)
            simple_collection.rels_ext.content.add(relation)
            if self.verbosity > self.v_normal:
                self.stdout.write("Adding hasMember %s relation on SimpleCollection\n" % (arrangement_object.pid))

        if not options['no-act']:
            try:
                simple_collection.save()
                self.stdout.write("Saved SimpleCollection %s(%s)\n" % (simple_collection.label, simple_collection.pid))
            except Exception as e:
                    if self.verbosity > self.v_none:
                        self.stdout.write("Error saving SimpleCollection %s: %s\n" % (simple_collection.label, e.message))
                        self.stdout.write("Deleting Arrangement pids so they will not be Orphans\n")
                    errors += 1
                    for pid in self.arrangement_pids:
                        self.repo.purge_object(pid)
                        if self.verbosity > self.v_none:
                            self.stdout.write("Deleting: %s\n" % (pid))
                        arrangement_saved -= 1




        if self.verbosity > self.v_normal:
                self.stdout.write("===RELS-EXT===\n")
                for entry in simple_collection.rels_ext.content:
                    self.stdout.write("%s" % list(entry))

        elif self.verbosity > self.v_none:
            self.stdout.write("TEST SimpleCollection %s\n" % (simple_collection.label))

        #print Summary
        self.stdout.write("SUMMARY\n=======\n")
        self.stdout.write("SimpleCollection: %s(%s)\n" % (simple_collection.label, simple_collection.pid))
        self.stdout.write("Master Collection Object: %s(%s)\n" % (self.master_obj.label, self.master_obj.pid))
        self.stdout.write("%s Records read from CSV file\n" % (csv_read))
        self.stdout.write("%s Records created\n" % (arrangement_saved))
        self.stdout.write("%s Errors\n" % (errors))