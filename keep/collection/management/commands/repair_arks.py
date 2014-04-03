from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from eulfedora.models import DigitalObjectSaveFailure
from eulxml.xmlmap import mods

from pidservices.djangowrapper.shortcuts import DjangoPidmanRestClient
from pidservices.clients import parse_ark

from keep.collection.models import CollectionObject
from keep.audio.models import AudioObject
from keep.common.fedora import Repository

LOG_LEVEL = ['QUIET', 'INFO', 'WARNING']

QUIET, INFO, WARNING = range(3)

class Command(BaseCommand):
    '''Repair missing ARKs for :class:`~keep.collection.models.CollectionObject` objects
    based on the correct ARK from PIDMAN.

    '''
    args = '[PID [PID...]]'
    help = '''Repair ARKs on Keep Collections or Audio objects.
    Optionally accepts a list of PIDs to be repaired.  If no pids are specified,
    will find all collection objects and attempt to repair them.'''

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
        self.pidman = DjangoPidmanRestClient()

        # populate list of objects to be processed
        objects = []
        for pid in args:
            try:
                obj = repo.get_object(pid=pid, type=CollectionObject)
                if obj.has_requisite_content_models:
                    objects.append(obj)
                else:
                    obj = repo.get_object(pid=pid, type=AudioObject)
                    if obj.has_requisite_content_models:
                        objects.append(obj)
            except Exception:
                self.log(message="Could not find Collection or Audio object for: %s" % pid)

        # get list of all collections from the repository
        # limited to the COLLECTION_CONTENT_MODEL as well as returns a Keep specific collection object
        if not args:
            objects = repo.get_objects_with_cmodel(CollectionObject.COLLECTION_CONTENT_MODEL, type=CollectionObject)

        if not objects:
            self.log(message="No Collections were found.")

        for obj in objects:
            self.repair_ark(obj)

        self.log(message="\n\n%s ARKs repaired\n%s ARKs were not repaired" % (self.repaired_count, self.unrepaired_count), no_label=True)

    def repair_ark(self, obj):
        ark_target = None
        try:
            ark_target = self.pidman.get_ark_target(noid=obj.noid, qualifier='')
        except:
            self.unrepaired_count += 1
            self.log(level=WARNING, message="Failed to find ARK target for %s" % (obj.pid))
            return


        parsed_ark = parse_ark(ark_target['access_uri'])
        naan = parsed_ark['naan']
        noid = parsed_ark['noid']

        if hasattr(obj, 'mods'):
            obj.mods.content.identifiers.extend([
                mods.Identifier(type='ark', text='ark:/%s/%s' % (naan, noid)),
                mods.Identifier(type='uri', text=ark_target['access_uri'])
                ])
        else:
            obj.dc.content.identifier_list(ark_target['access_uri'])

        if self.options['dry_run']:
            self.unrepaired_count += 1
            self.log(message='ARK target found for %s' % obj.pid)
            return

        # save the collection object w/ updated ark
        try:
            self.log(level=INFO, message="Attempting to save %s" % obj.pid)
            obj.save(logMessage='Fixing missing ARK')
            self.repaired_count += 1
        except DigitalObjectSaveFailure:
            self.log(message="An error occurred while saving %s" % (obj.pid))

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
