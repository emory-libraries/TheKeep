from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import csv


class Command(BaseCommand):

    #Set up additional options
    option_list = BaseCommand.option_list + (
        make_option('--noact', '-n',
            action='store_true',
            dest='no-act',
            default=False,
            help='Does not create PIDs or ingest anything into Fedora. Only parses file and outputs results'),
    )

    args = '<CSV file>'
    help = 'Load csv arrangement file into Fedora'

    def handle(self, *args, **options):
        #looks for file param
        try:
            file =  args[0]
        except IndexError:
            raise CommandError("No File specified")

        #try to read file into a dict and assign the field names
        try:
            reader = csv.DictReader(open(file, 'rb'),
                                    fieldnames=["id","checksum","filename","rec_type","file_type",
                                                "creator","attrib","created","modified","computer","size"])
        except IOError:
            raise CommandError("Could not read file %s" % file)

        reader.next() # skip the header row
        
        #read each field
        for row in reader:
            id = row["id"]
            checksum = row["checksum"]
            filename = row["filename"]
            rec_type = row["rec_type"]
            file_type = row["file_type"]
            creator = row["creator"]
            attrib = row["attrib"]
            created = row["created"]
            modified = row["modified"]
            computer = row["computer"]
            size = row["size"]

            #remove print lines once more logic is added
            print "**********"
            print " %s %s %s %s %s %s %s %s %s %s %s" % \
                  (id, checksum, filename, rec_type, file_type, creator, attrib, created, modified, computer, size)
            print "**********"

