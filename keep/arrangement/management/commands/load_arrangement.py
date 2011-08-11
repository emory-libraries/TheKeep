import csv
from optparse import make_option

from eulfedora.rdfns import relsext as relsextns

from django.core.management.base import BaseCommand, CommandError

from keep.arrangement.models import ArrangementObject
from keep.collection.models import CollectionObject, SimpleCollection
from keep.common.fedora import Repository

class Command(BaseCommand):

    #Set up additional options
    option_list = BaseCommand.option_list + (
        make_option('--noact', '-n',
            action='store_true',
            dest='no-act',
            default=False,
            help='Does not create PIDs or ingest anything into Fedora. Only parses file and outputs results'),
        make_option('--append', '-a',
            action='store',
            dest='append',
            help='Appends to the SimpleCollection specified by pid, does not create a new SimpleCollection'),
    )

    args = '<CSV file> <master collection pid> <new simple collection name>'
    help = '''Read CSV file and creates (or adds to) a Simple Collection and associated ArrangementObjects
    with the SimpleCollection and the Master collection'''

    def create_arrangement(self):
        # set values on arrangement object
        obj = self.repo.get_object(type=ArrangementObject)
        obj.label = self.filename
        obj.filetech.content.local_id = self.id
        obj.filetech.content.md5 = self.checksum
        obj.filetech.content.computer = self.computer
        obj.filetech.content.path = self.filename
        obj.filetech.content.attributes = self.attrib
        obj.filetech.content.created = self.created
        obj.filetech.content.modified = self.modified
        obj.filetech.content.type = self.rec_type
        obj.filetech.content.creator = self.creator

        # set association to master collection
        relation = (obj.uriref, relsextns.isMemberOf, self.master_obj.uriref)
        obj.rels_ext.content.add(relation)
        if self.verbosity > self.v_normal:
            self.stdout.write("Adding %s isMemberOf %s relation on ArrangementObject\n" % (obj.label, self.master_obj.pid))

        return obj

    def handle(self, *args, **options):
        self.v_normal = 1        # 1 = normal, 2 = all
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

        #if -a or --append is used the new SimpleCollection name is ignored
        try:
            if not options["append"]:
                self.simple_collection_name =  args[2]
            else:
                self.simple_collection_pid = options["append"]

        except IndexError:
            raise CommandError("An existing SimpleCollection pid must be specified with the -a option or \
            a new SimpleCollection name must be specified as an argument")

        #If Master collection does not exist then raise an exception
        self.master_obj = self.repo.get_object(type = CollectionObject, pid=self.master_pid)

        if not self.master_obj.exists:
            raise CommandError("Master Collection %s does not exist" % (self.master_pid))
        else:
            self.stdout.write("Using Master Collection: %s(%s)\n" % (self.master_obj.label, self.master_obj.pid))

        #Get or create SimpleColletion object
        #TODO Not sure why I have to do a try block to prevent a 404 here when I don't in other places
        try:
            if options["append"]:
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
            self.stdout.write("Reading CSV: %s\n" % (file))
        except IOError:
            raise CommandError("Could not read file %s" % file)


        # skip the header row in CSV file
        reader.next()
        
        #read each field
        for row in reader:
            self.id = row["id"]
            self.checksum = row["checksum"]
            self.filename = row["filename"]
            self.rec_type = row["rec_type"]
            self.file_type = row["file_type"]
            self.creator = row["creator"]
            self.attrib = row["attrib"]
            self.created = row["created"]
            self.modified = row["modified"]
            self.computer = row["computer"]
            self.size = row["size"]

            arrangement_object = self.create_arrangement()

            if not options['no-act']:
                arrangement_object.save()
                self.stdout.write("Saved ArrangementObject %s(%s)\n" % (arrangement_object.label, arrangement_object.pid))
                if self.verbosity > self.v_normal:
                    self.stdout.write("===RELS-EXT===\n")
                    for entry in arrangement_object.rels_ext.content:
                        self.stdout.write("%s" % list(entry))
            else:
                self.stdout.write("TEST ArrangementObject %s\n" % (arrangement_object.label))

            #Add each ArrangementObject to the SimpleCollection
            relation = (simple_collection.uriref, relsextns.hasMember, arrangement_object.uriref)
            simple_collection.rels_ext.content.add(relation)
            if self.verbosity > self.v_normal:
                self.stdout.write("Adding hasMember %s relation on SimpleCollection\n" % (arrangement_object.pid))

        if not options['no-act']:
            simple_collection.save()
            self.stdout.write("Saved SimpleCollection %s(%s)\n" % (simple_collection.label, simple_collection.pid))
            if self.verbosity > self.v_normal:
                    self.stdout.write("===RELS-EXT===\n")
                    for entry in simple_collection.rels_ext.content:
                        self.stdout.write("%s" % list(entry))

        else:
            self.stdout.write("TEST SimpleCollection %s\n" % (simple_collection.label))