import logging
from optparse import make_option

from eulfedora.rdfns import relsext as relsextns

from django.core.management.base import BaseCommand, CommandError

#from keep.arrangement.models import ArrangementObject
from keep.collection.models import CollectionObject, SimpleCollection
#from keep.common.eadmap import Series
from keep.common.fedora import Repository

logger = logging.getLogger(__name__)

#All Rushdie Content Modles
CONTENT_MODELS =[
    'info:fedora/emory-control:Rushdie-CerpAccount-1.0',
    'info:fedora/emory-control:Rushdie-CerpMailbox-1.0',
    'info:fedora/emory-control:Rushdie-Fax-1.0',
    'info:fedora/emory-control:Rushdie-MailboxEntry-1.0',
    'info:fedora/emory-control:Rushdie-MarblMacFile-1.0',
    'info:fedora/emory-control:RushdieMetadata-1.0',
    'info:fedora/emory-control:RushdieResearcherAllowed-1.0',
    'info:fedora/emory-control:RushdieResearcherRestricted-1.0'
]


class Command(BaseCommand):
    '''Migrates old-style Rushdie objects to new-style. This includes adding
    The objects to a SimpleCollection, converting old datastreams to new datastreams
    and associating each object to the main collection'''

    #Set up additional options
    option_list = BaseCommand.option_list + (
        make_option('--noact', '-n',
            action='store_true',
            dest='no-act',
            default = False,
            help='Do not do anything'),
        make_option('--simple-collection-step', '-S',
            action='store_true',
            dest='simple-collection-step',
            default = False,
            help='Only run the step to collect objects into a SimpleCollection.  \
            If Simple Collection exists it will use  the existing one'),
#        make_option('--datastreams', '-D',
#            action='store_true',
#            dest='datastreams-step',
#            default = False,
#            help='Only run the step to convert datastreams'),
#        make_option('--master-collection-step', '-M',
#            action='store_true',
#            dest='master-collection-step',
#            default = False,
#            help='Only run the step to associate object with master collection'),
#        make_option('--master-collection-pid', '-m',
#            action='store',
#            dest='master-collection-pid',
#            default = "",
#            help='Pid of the Master Collection'),
        make_option('--simple-collection', '-s',
            action='store',
            dest='simple-collection',
            default = "",
            help='Label of the SimpleCollection'),
    )

    help = __doc__

    def _get_unique_objects(self, args):
        all_objs = []
        #if pids specified  only get thoes objects
        if args:
            pids = set(args)
            for pid in pids:
                try:
                    obj = self.repo.get_object(pid = pid)
                    if obj.exists:
                        all_objs.append(obj)
                    else:
                        if self.verbosity > self.v_none:
                            self.stdout.write("pid %s does not exist\n" % (pid))

                except Exception as e:
                    if self.verbosity > self.v_none:
                        self.stdout.write("Error getting pid %s : %s\n" % (pid, e))
        else:
            pids = set()
            #lookup all rushdie pids
            for cm in CONTENT_MODELS:
                try:
                    objs = self.repo.get_objects_with_cmodel(cm)
                except Exception as e:
                    if self.verbosity > self.v_none:
                        self.stdout.write("Error getting pids with ContentModle %s : %s\n" % (cm, e))
                for obj in objs:
                    try:
                        pids.add(obj.pid)
                    except Exception as e:
                        if self.verbosity > self.v_none:
                            self.stdout.write("Error accessing pid %s : %s\n" % (obj.pid, e))
            for pid in pids:
                try:
                    all_objs.append(self.repo.get_object(pid=pid))
                except Exception as e:
                    if self.verbosity > self.v_none:
                        self.stdout.write("Error getting pid  %s : %s\n" % (pid, e))

        return all_objs

    #Adds pids to sc (SimpleCollection) using a hasMember relation on the SimpleCollection
    def _add_to_simple_collection(self,  obj):
        #logic to add to simple collection
        if self.verbosity > self.v_normal:
            self.stdout.write("Adding %s to SimpleCollection %s using hasMember relation\n" % (obj.pid, self.simple_collection.label))
        relation = (self.simple_collection.uriref, relsextns.hasMember, obj.uriref)
        self.simple_collection.rels_ext.content.add(relation)

    #Converts the datastreams of the object to new-style
#   def _convert_ds(self, obj):
#        #logic to convert datastreams

    #Associates obj with master collection object using a isMemberOf relation on obj
#    def _add_to_master_collection(self, obj):
#        print "Adding %s to Master Collection" % obj.pid
#        return obj
#        #logic to add to master collection


    def handle(self, *args, **options):
        #setup verbosity
        #0 = none, 1 = normal, 2 = all
        self.v_none = 0
        self.v_normal = 1

        if 'verbosity' in options:
            self.verbosity = int(options['verbosity'])
        else:
            self.verbosity = self.v_normal

        #Create the repo
        self.repo = Repository()

        #Check options

        #if no steps are specified then run all steps
        #if not options["simple-collection-step"] and not options["master-collection-step"]:
        if not options["simple-collection-step"]:
            options["simple-collection-step"] = True
#            options["master-collection-step"] = True

        #This step requires simeple collection Label
        if options["simple-collection-step"]:
            if not options["simple-collection"]:
                raise CommandError("When running SimpleCollection step SimpleCollection Label is required")
            else:
                #lookup Simplecollection
                try:
                    sc_list = list(self.repo.find_objects(label__exact=options["simple-collection"], type=SimpleCollection))
                    if len(sc_list) > 1: # something is wrong need to investigate
                        raise CommandError("More than one SimpleCollection with Label %s exists" % options["simple-collection"])
                    elif len(sc_list) == 1: # use this as the simple collection
                        self.simple_collection = sc_list[0]
                    elif len(sc_list) == 0: #create new simple collection
                        self.simple_collection = self.repo.get_object(type=SimpleCollection)
                        self.simple_collection.label = options["simple-collection"]
                except Exception as e:
                    if not isinstance(e, CommandError):
                        raise CommandError("Could not obtain requested SimpleCollection %s : %s" % (options["simple-collection"], e))
                    else:
                        raise e

        #This step requires master collection pid
#        if options["master-collection-step"]:
#            if not options["master-collection-pid"]:
#                raise CommandError("When running Master Collection step Master Collection PID is required")
#            else:
#                try:
#                    self.master_collection = self.repo.get_object(pid = options["master-collection-pid"], type=CollectionObject)
#                    if not self.master_collection.exists:
#                        raise CommandError("Master Collection %s does not exist" % options["master-collection-pid"])
#                except Exception as e:
#                    if not isinstance(e, CommandError):
#                        raise CommandError("Could not obtain requested Master Collection %s : %s" % (options["master-collection-pid"], e))
#                    else: raise e


        #All objects to be migrated
        self.all_objs = self._get_unique_objects(args)

        #Process each object
        for obj in self.all_objs:
            if self.verbosity > self.v_none:
                self.stdout.write( "Processing %s\n" % (obj.pid))

            if options["simple-collection-step"]:
                self._add_to_simple_collection(obj)


#            if options["master-collection-step"]:
#                obj = self._add_to_master_collection(obj)

            #Save object
#            if not options["no-act"]:
#                obj.save()
#            else:
#                print "NOT SAVING OBJECT"

        #Print RELS-EXT
        if self.verbosity > self.v_normal:
            self.stdout.write("===RELS-EXT===\n")
            for entry in self.simple_collection.rels_ext.content:
                self.stdout.write("%s\n" % list(entry))

        #Save SimpleCollection
        if not options["no-act"]:
            self.simple_collection.save()
            if self.verbosity > self.v_none:
                self.stdout.write("Saved %s(%s)\n" % (self.simple_collection.label, self.simple_collection.pid) )
        else:
            if self.verbosity > self.v_none:
                self.stdout.write("Test saving %s(%s)\n" % (self.simple_collection.label, self.simple_collection.pid) )