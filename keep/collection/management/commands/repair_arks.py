from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from eulfedora.models import DigitalObjectSaveFailure
from eulcm.models.collection.v1_1 import Collection
from eulxml.xmlmap import mods

from pidservices.djangowrapper.shortcuts import DjangoPidmanRestClient
from pidservices.clients import parse_ark

from keep.collection.models import CollectionObject
from keep.common.fedora import Repository
from keep import localsettings

LOG_LEVEL = ['QUIET', 'INFO', 'WARNING']

QUIET, INFO, WARNING = range(3)

class Command(BaseCommand):
    '''Repair missing ARKs for :class:`~keep.collection.models.CollectionObject` objects
    based on the correct ARK from PIDMAN.

    '''
    args = '[PID [PID...]]'
    help = 'Repair ARKs on Keep Collections. It optionally accepts a list of PIDs to be repaired.'

    option_list = BaseCommand.option_list + (
        make_option('--dry-run',
            dest='dry_run',
            action='store_true',
            default=False,
            help='Report which ARKs would be repaired'),
        )

    def handle(self, *args, **options):
        self.options = options
        self.repaired_count = 0
        self.unrepaired_count = 0

        repo = Repository()
        pidman = DjangoPidmanRestClient()

        #populate collections list only of the object has the cmodel
        collections = []
        for pid in args:
            try:
                coll_object = repo.get_object(pid=pid, type=CollectionObject)
                if coll_object.has_requisite_content_models():
                    collections.append(coll_object)
            except:
                self.log(message="Could not find Collection: %s" % pid)
        
        # get list of collections from the repository
        # limited to the COLLECTION_CONTENT_MODEL as well as returns a Keep specific collection object
        if not args:
            collections = repo.get_objects_with_cmodel(CollectionObject.COLLECTION_CONTENT_MODEL, type=CollectionObject)
        
        if not collections:
            self.log(message="No Collections were found.")

        for coll_obj in collections:
            self.repair_ark(collection_object=coll_obj)

        self.log(message="\n\n%s ARKs repaired\n%s ARKs were not repaired" % (self.repaired_count, self.unrepaired_count), no_label=True)

    def repair_ark(self, collection_object):
        pidman = DjangoPidmanRestClient()

        ark_target = None
        try: 
            ark_target = pidman.get_ark_target(noid=collection_object.noid, qualifier='')
        except:
            self.unrepaired_count += 1
            self.log(level=WARNING, message="Failed to find ARK target for %s" % (collection_object.pid))
            return


        parsed_ark = parse_ark(ark_target['access_uri'])
        naan = parsed_ark['naan']
        noid = parsed_ark['noid']

        if hasattr(collection_object, 'mods'):
            collection_object.mods.content.identifiers.extend([
                mods.Identifier(type='ark', text='ark:/%s/%s' % (naan, noid)),
                mods.Identifier(type='uri', text=ark_target['access_uri'])
                ])
        else:
            collection_object.dc.content.identifier_list(ark_target['access_uri'])

        if self.options['dry_run']:
            self.unrepaired_count += 1
            self.log(message='ARK target found for %s' % collection_object.pid)
            return

        # save the collection object w/ updated ark
        try:
            self.log(level=INFO, message="Attempting to save %s" % collection_object.pid)
            collection_object.save(logMessage='Fixing missing ARK')
            self.repaired_count += 1
        except DigitalObjectSaveFailure:
            self.log(message="An error occurred while saving %s" % (collection_object.pid))

    def log(self, level=INFO, message='', no_label=False):
        '''
        Convenience log function. WARNING level is only logged if the --verbosity flag is set to 2. 
        INFO level is default and always logged. no_label can be set to True if a WARNING or INFO label
        is not desired.
        '''
        if level == WARNING and not int(self.options['verbosity']) == WARNING:
            return
        output_str = ''
        if not no_label:
            output_str = '%s: ' % LOG_LEVEL[level]
        print "%s%s" % (output_str, message)
