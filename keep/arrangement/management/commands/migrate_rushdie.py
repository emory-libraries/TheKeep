from getpass import getpass
import logging
from rdflib import URIRef
from optparse import make_option
from xml.etree import ElementTree

from eulfedora.rdfns import relsext as relsextns
from eulfedora.rdfns import model
from eulcm.xmlmap.boda import FileMasterTech_Base

from django.core.management.base import BaseCommand, CommandError

from keep.arrangement.models import ArrangementObject
from keep.collection.models import CollectionObject, SimpleCollection
from keep.common.eadmap import Series
from keep.common.fedora import Repository

logger = logging.getLogger(__name__)

#All Rushdie Content Modles
CONTENT_MODELS = [
    'info:fedora/emory-control:Rushdie-CerpAccount-1.0',
    'info:fedora/emory-control:Rushdie-CerpMailbox-1.0',
    'info:fedora/emory-control:Rushdie-Fax-1.0',
    'info:fedora/emory-control:Rushdie-MailboxEntry-1.0',
    'info:fedora/emory-control:Rushdie-MarblMacFile-1.0'
]


class Command(BaseCommand):
    '''Migrates old-style Rushdie objects to new-style. This includes adding
    The objects to a SimpleCollection, converting old datastreams to new datastreams
    and associating each object to the main collection'''

    def get_password_option(option, opt, value, parser):
        setattr(parser.values, option.dest, getpass())

    #Set up additional options
    option_list = BaseCommand.option_list + (
        make_option('--noact', '-n',
            action='store_true',
            dest='no-act',
            default=False,
            help='Do not do anything'),
        make_option('--simple-collection-step', '-S',
            action='store_true',
            dest='simple-collection-step',
            default=False,
            help='Only run the step to collect objects into a SimpleCollection.  \
            If Simple Collection exists it will use  the existing one'),
        make_option('--datastreams', '-D',
            action='store_true',
            dest='datastreams-step',
            default=False,
            help='Only run the step to convert datastreams'),
        make_option('--master-collection-pid', '-m',
            action='store',
            dest='master-collection-pid',
            default="",
            help='Pid of the Master Collection'),
        make_option('--simple-collection', '-s',
            action='store',
            dest='simple-collection',
            default="",
            help='Label of the SimpleCollection'),
        make_option('--username', '-u',
            dest='username',
            action='store',
            help='''Username to connect to fedora'''),
        make_option('--password',
            dest='password',
            action='callback', callback=get_password_option,
            help='''Prompt for password required when username used'''),
    )

    help = __doc__

    def _create_series_lookup(self):
        #series / subseries info
        series = {}

        #exist query params
        return_fields = ['eadid']
        search_fields = {'eadid': 'rushdie1000'}

        queryset = Series.objects.also(*return_fields).filter(**search_fields)
        for s in queryset:
            #series info
            series[s.title] = {}
            series[s.title]['series_info'] = {}
            series[s.title]['series_info']['id'] = s.id
            series[s.title]['series_info']['short_id'] = s.short_id
            series[s.title]['series_info']['base_ark'] = s.eadid.url
            series[s.title]['series_info']['uri'] = "https://findingaids.library.emory.edu/documents/%s/%s" % \
                (s.eadid.value, s.short_id)
            #subseries info
            if s.subseries:
                series[s.title]['subseries_info'] = {}
                for sub in s.subseries:
                    series[s.title]['subseries_info'][sub.title] = {}
                    series[s.title]['subseries_info'][sub.title]['id'] = sub.id
                    series[s.title]['subseries_info'][sub.title]['short_id'] = sub.short_id
                    series[s.title]['subseries_info'][sub.title]['base_ark'] = s.eadid.url
                    series[s.title]['subseries_info'][sub.title]['uri'] = "https://findingaids.library.emory.edu/documents/%s/%s/%s" % \
                    (s.eadid.value, s.short_id, sub.short_id)
        return series

    def _get_unique_objects(self, args):
        all_objs = []
        #if pids specified  only get thoes objects
        if args:
            pids = set(args)
            for pid in pids:
                try:
                    obj = self.repo.get_object(pid=pid, type=ArrangementObject)
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
                    all_objs.append(self.repo.get_object(pid=pid, type=ArrangementObject))
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

#   Converts the datastreams of the object to new-style
    def _convert_ds(self, obj, master, series_lookup, noact):
        #convert MARBL-MACTECH to FilemasterTech
        mm = obj.getDatastreamObject("MARBL-MACTECH")
        if mm:
            if self.verbosity > self.v_none:
                self.stdout.write("Converting MARBL-MACTECH\n")
            etree = ElementTree.fromstring(mm.content)
            ns = 'info:fedora/emory-control:Rushdie-MacFsData-1.0'

            md5 = etree.find('.//{%s}md5' % ns)
            files = etree.findall('.//{%s}file' % ns)

            for i, file in enumerate(files):

                computer = file.find('.//{%s}computer' % ns)
                path = file.find('.//{%s}path' % ns)
                rawpath = file.find('.//{%s}rawpath' % ns)
                attrib = file.find('.//{%s}attributes' % ns)
                created = file.find('.//{%s}created' % ns)
                modified = file.find('.//{%s}modified' % ns)
                type = file.find('.//{%s}type' % ns)
                creator = file.find('.//{%s}creator' % ns)

                #Make new file section
                obj.filetech.content.file.append(FileMasterTech_Base())
                obj.filetech.content.file[i].md5 = md5.text if md5 is not None else ""
                obj.filetech.content.file[i].computer = computer.text if computer is not None else ""
                obj.filetech.content.file[i].path = path.text if path is not None else ""
                obj.filetech.content.file[i].rawpath = rawpath.text if rawpath is not None else ""
                obj.filetech.content.file[i].attributes = attrib.text if attrib is not None else ""
                obj.filetech.content.file[i].created = created.text if created is not None else ""
                obj.filetech.content.file[i].modified = modified.text if modified is not None else ""
                obj.filetech.content.file[i].type = type.text if type is not None else ""
                obj.filetech.content.file[i].creator = creator.text if creator is not None else ""

                obj.dc.content.title = obj.filetech.content.file[0].path.rpartition("/")[2]
                obj.label = obj.filetech.content.file[0].path.rpartition("/")[2]

            if not noact:
                obj.api.purgeDatastream(obj.pid, "MARBL-MACTECH")
                if self.verbosity > self.v_normal:
                    self.stdout.write("Removed MARBL-MACTECH\n")
            else:
                if self.verbosity > self.v_normal:
                    self.stdout.write("TEST Removed MARBL-MACTECH\n")

        #convert MARBL-ANALYSIS to MODS
        ma = obj.getDatastreamObject("MARBL-ANALYSIS")
        if ma:
            if self.verbosity > self.v_none:
                self.stdout.write("Converting MARBL-ANALYSIS\n")
            etree = ElementTree.fromstring(ma.content)
            ns = 'info:fedora/emory-control:Rushdie-MarblAnalysis-1.0'
            series = etree.find('.//{%s}series' % ns)
            series = series.text if series is not None else ""
            subseries = etree.find('.//{%s}subseries' % ns)
            subseries = subseries.text if subseries is not None else ""
            verdict = etree.find('.//{%s}verdict' % ns)
            verdict = verdict.text if verdict is not None else ""

            #Translate verdict to code to store in Rights
            status_code_map = {
                "META": "13",
                "VIRTUAL": "2",
                "EMULATION ONLY": "2",
                "EMULATION": "2",
                "AS IS": "2",
                "RESTRICTED": "4",
                "REDACTED": "12"
            }
            try:
                code = status_code_map.get(verdict.upper(), "") if verdict else ""
                obj.rights.content.create_access_status()
                obj.rights.content.access_status.code = code
            except KeyError:
                pass

            #Map series and sub series

            #Specal Cases for identifying series info
            if series == "Writings":
                series = "Writings by Rushdie"

            if "Correspondence" in series:
                series = "Correspondence"

            if subseries == "Family papers":
                series = "Personal papers"

            if subseries == "Other Writings":
                series = "Writings by Rushdie"

            if subseries == "Non Fiction":
                subseries = "Nonfiction"

            if "Journal" in series or "Journal" in subseries:
                series = "Journals, appointment books, and notebooks"

            if series in series_lookup and \
                "subseries_info" in series_lookup[series] and \
                subseries in series_lookup[series]["subseries_info"]:

                obj.mods.content.create_series()
                obj.mods.content.series.create_series()

                obj.mods.content.series.title = subseries
                obj.mods.content.series.uri = series_lookup[series]["subseries_info"][subseries]["uri"]
                obj.mods.content.series.base_ark = series_lookup[series]["subseries_info"][subseries]["base_ark"]
                obj.mods.content.series.full_id = series_lookup[series]["subseries_info"][subseries]["id"]
                obj.mods.content.series.short_id = series_lookup[series]["subseries_info"][subseries]["short_id"]

                obj.mods.content.series.series.title = series
                obj.mods.content.series.series.uri = series_lookup[series]["series_info"]["uri"]
                obj.mods.content.series.series.base_ark = series_lookup[series]["series_info"]["base_ark"]
                obj.mods.content.series.series.full_id = series_lookup[series]["series_info"]["id"]
                obj.mods.content.series.series.short_id = series_lookup[series]["series_info"]["short_id"]

            elif series in series_lookup and subseries:
                obj.mods.content.create_series()
                obj.mods.content.series.create_series()

                obj.mods.content.series.title = subseries

                obj.mods.content.series.series.title = series
                obj.mods.content.series.series.uri = series_lookup[series]["series_info"]["uri"]
                obj.mods.content.series.series.base_ark = series_lookup[series]["series_info"]["base_ark"]
                obj.mods.content.series.series.full_id = series_lookup[series]["series_info"]["id"]
                obj.mods.content.series.series.short_id = series_lookup[series]["series_info"]["short_id"]

            elif series in series_lookup:
                obj.mods.content.create_series()

                obj.mods.content.series.title = series
                obj.mods.content.series.uri = series_lookup[series]["series_info"]["uri"]
                obj.mods.content.series.base_ark = series_lookup[series]["series_info"]["base_ark"]
                obj.mods.content.series.full_id = series_lookup[series]["series_info"]["id"]
                obj.mods.content.series.short_id = series_lookup[series]["series_info"]["short_id"]

            else:
                if series and subseries:
                    obj.mods.content.create_series()
                    obj.mods.content.series.create_series()

                    obj.mods.content.series.title = subseries

                    obj.mods.content.series.series.title = series

                elif series:
                    obj.mods.content.create_series()
                    obj.mods.content.series.title = series

            #Remove Datastreams
            if not noact:
                obj.api.purgeDatastream(obj.pid, "MARBL-ANALYSIS")
                if self.verbosity > self.v_normal:
                    self.stdout.write("Removed MARBL-ANALYSIS\n")
            else:
                if self.verbosity > self.v_normal:
                    self.stdout.write("TEST Removed MARBL-ANALYSIS\n")

#        Add  Arrangement Relation
        relation = (obj.uriref, model.hasModel,
            URIRef("info:fedora/emory-control:Arrangement-1.0"))
        obj.rels_ext.content.add(relation)

        #Add  relation to master collection
        relation = (obj.uriref, relsextns.isMemberOf, master.uriref)
        obj.rels_ext.content.add(relation)

        #Add Content Model based on Rights
        allowed = (obj.uriref, model.hasModel,
            URIRef("info:fedora/emory-control:ArrangementAccessAllowed-1.0"))
        restricted = (obj.uriref, model.hasModel,
            URIRef("info:fedora/emory-control:ArrangementAccessRestricted-1.0"))

        if getattr(obj.rights.content.access_status, "code", None) == "2":
            obj.rels_ext.content.add(allowed)
        elif getattr(obj.rights.content.access_status, "code", None):
            obj.rels_ext.content.add(restricted)

        return obj

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
        repo_args = {}
        if options.get('username') is not None:
            repo_args['username'] = options.get('username')
        if options.get('password') is not None:
            repo_args['password'] = options.get('password')
        self.repo = Repository(**repo_args)

        #Check options

        #if no steps are specified then run all steps
        if not options["simple-collection-step"] and not options["datastreams-step"]:
            options["simple-collection-step"] = True
            options["datastreams-step"] = True

        #This step requires simeple collection Label
        if options["simple-collection-step"]:
            if not options["simple-collection"]:
                raise CommandError("When running SimpleCollection step SimpleCollection Label is required")
            else:
                #lookup Simplecollection
                try:
                    sc_list = list(self.repo.find_objects(label__exact=options["simple-collection"], type=SimpleCollection))
                    if len(sc_list) > 1:  # something is wrong need to investigate
                        raise CommandError("More than one SimpleCollection with Label %s exists" % options["simple-collection"])
                    elif len(sc_list) == 1:  # use this as the simple collection
                        self.simple_collection = sc_list[0]
                    elif len(sc_list) == 0:  # create new simple collection
                        self.simple_collection = self.repo.get_object(type=SimpleCollection)
                        self.simple_collection.label = options["simple-collection"]
                        self.simple_collection.dc.content.title = options["simple-collection"]
                        self.simple_collection.mods.content.create_restrictions_on_access()
                        self.simple_collection.mods.content.restrictions_on_access.text = "Accessioned"
                except Exception as e:
                    if not isinstance(e, CommandError):
                        raise CommandError("Could not obtain requested SimpleCollection %s : %s" % (options["simple-collection"], e))
                    else:
                        raise e

        if options["datastreams-step"]:
            if not options["master-collection-pid"]:
                raise CommandError("When running Datastream step Master collection pid is required")
            else:
                try:
                    self.master_collection = self.repo.get_object(pid=options["master-collection-pid"],
                        type=CollectionObject)
                    if not self.master_collection.exists:
                        raise CommandError("Master Collection %s does not exist" \
                            % options["master-collection-pid"])
                except Exception as e:
                    raise CommandError("Could not obtain requested Master Collection %s : %s" \
                        % (options["master-collection-pid"], e))

        #Create lookup for series
        series_lookup = self._create_series_lookup()

        #All objects to be migrated
        self.all_objs = self._get_unique_objects(args)

        #Process each object
        for obj in self.all_objs:
            if self.verbosity > self.v_none:
                self.stdout.write("Processing %s\n" % (obj.pid))

            if options["simple-collection-step"]:
                self._add_to_simple_collection(obj)

            if options["datastreams-step"]:
                obj = self._convert_ds(obj, self.master_collection, series_lookup, options["no-act"])
                if self.verbosity > self.v_normal:
                    self.stdout.write("===FilemasterTech===\n")
                    self.stdout.write("%s\n" % (obj.filetech.content.serialize()))
                    self.stdout.write("=== RELS-EXT===\n")
                    for entry in obj.rels_ext.content:
                        self.stdout.write("%s\n" % list(entry))
                    self.stdout.write("===Rights===\n")
                    self.stdout.write("%s\n" % (obj.rights.content.serialize()))
                    self.stdout.write("===Mods===\n")
                    self.stdout.write("%s\n" % (obj.mods.content.serialize()))

            #Save object
            obj.owner = "thekeep-project"
            if self.verbosity > self.v_normal:
                self.stdout.write("owner:%s\n" % obj.owner)
            if not options["no-act"]:
                obj.save()
                if self.verbosity > self.v_none:
                    self.stdout.write("Saving %s\n" % obj.pid)
            else:
                if self.verbosity > self.v_none:
                    self.stdout.write("TEST Saving Object\n")

        #Print RELS-EXT forSimple Collection
        if options["simple-collection-step"]:
            if self.verbosity > self.v_normal:
                self.stdout.write("===RELS-EXT===\n")
                for entry in self.simple_collection.rels_ext.content:
                    self.stdout.write("%s\n" % list(entry))
                self.stdout.write("===DC===\n")
                self.stdout.write("%s\n" % self.simple_collection.dc.content.serialize())
                self.stdout.write("===MODS===\n")
                self.stdout.write("%s\n" % self.simple_collection.mods.content.serialize())

            #Save SimpleCollection
            if not options["no-act"]:
                self.simple_collection.save()
                if self.verbosity > self.v_none:
                    self.stdout.write("Saved %s(%s)\n" % \
                        (self.simple_collection.label, self.simple_collection.pid))
            else:
                if self.verbosity > self.v_none:
                    self.stdout.write("Test saving %s(%s)\n" %
                        (self.simple_collection.label, self.simple_collection.pid))
