from datetime import datetime
from optparse import make_option
import os
from time import time

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    '''Clean up any files uploaded for ingest older than a specified duration.

    Uses directory and file age configurations from django settings.
    '''
    help = __doc__

    option_list = BaseCommand.option_list + (
        make_option('--dry-run', '-n',
            dest='dryrun',
            action='store_true',
            help='''Report on what would be done, but don't actually delete any files'''),
        )

    def handle(self, *args, **options):
        verbosity = int(options['verbosity'])    # 1 = normal, 0 = minimal, 2 = all
        v_normal = 1

        # check for required settings
        if not hasattr(settings, 'INGEST_STAGING_TEMP_DIR'):
            raise CommandError('INGEST_STAGING_TEMP_DIR setting is missing')
        if not hasattr(settings, 'INGEST_STAGING_KEEP_AGE'):
            raise CommandError('INGEST_STAGING_KEEP_AGE setting is missing')
        
        dir = settings.INGEST_STAGING_TEMP_DIR
        max_age = settings.INGEST_STAGING_KEEP_AGE

        if verbosity >= v_normal:
            print "Cleaning up files in %s older than %s seconds" % (dir, max_age)

        # get a list of files for checking
        try:
            files = os.listdir(dir)
        except OSError as e:
            raise CommandError('Failure reading configured directory %s:\n%s' % \
                               (dir, e))

        # loop through any files and delete ones older than configured keep duration
        errored = 0
        removed = 0
        for file in files:
            filepath = os.path.join(dir, file)
            stat = os.stat(filepath)
            # description for output messages
            file_lastmodified = "'%s' last modified %s" % (file,
                                        datetime.utcfromtimestamp(stat.st_mtime))
            # file modification time plus max age is older than the current time - delete
            if stat.st_mtime + max_age < time():
                if verbosity >= v_normal:
                    print "%s -- removing" % file_lastmodified
                if not options['dryrun']:
                    try:
                        os.unlink(filepath)
                        removed += 1
                    except OSError as e:
                        # if there is a problem deleting a file, report but keep going
                        if verbosity >= v_normal:
                            print "Error removing file '%s': %s" % (file, e)
                        errored += 1
            else:
                if verbosity > v_normal:
                    print "%s -- not removing" % file_lastmodified

        # summarize what was done
        if verbosity >= v_normal:
            print "%d file(s) checked" % len(files)
            print "%d file(s) removed" % removed
            print "%d error(s)" % errored

