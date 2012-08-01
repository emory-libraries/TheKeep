from django.core.management.base import BaseCommand

from keep.audio.models import AudioObject
from keep.audio.tasks import queue_access_copy

# This command is structured with the intention that it could be generalized
# to handle more than just AudioObjects. For now, module dependencies
# complicate that, but we should move in that direction as new types want
# access copy generation.

class Command(BaseCommand):
    '''Generate access copies for PIDs specified on the command line.'''
    help = __doc__

    def handle(self, *args, **options):
        self.verbosity = options['verbosity']
        self.repo = Repository()

        for pid in args:
            self.process_pid(pid)

    def process_pid(self, pid):
        '''Process a single PID by looking it up in the repository, figuring
        out what kind of processing it needs based on its object type, and
        doing that.
        '''

        obj = self.repo.get_object(pid=pid, type=repo.infer_object_subtype)
        if not obj.exists:
            if self.verbosity >= 1:
                print "No such PID; skipped:", pid
                return

        if isinstance(obj, AudioObject):
            if self.verbosity >= 2:
                print "Generating audio access copy:", pid
            queue_access_copy(obj)
        else:
            if self.verbosity >= 1:
                print "Unhandled  object type; skipped:", pid
