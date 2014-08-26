# file keep/audio/management/commands/dc_cleanup.py
# 
#   Copyright 2010 Emory University General Library
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.paginator import Paginator
from getpass import getpass
from optparse import make_option
from collections import defaultdict
from eulfedora.server import Repository
from keep.audio.models import AudioObject


class Command(BaseCommand):
    '''Cleanup DC datastream by calling _update_dc on object and then saving when there is a change
    '''
    args = "[pid pid ...]"
    help = __doc__

    option_list = BaseCommand.option_list + (
        make_option('--noact', '-n',
                    action='store_true',
                    default=False,
                    help='Reports the pid(s) and total number of objects that would be processed but does not save anything.'),
        make_option('--username',
                    action='store',
                    help='Username of fedora user to connect as'),
        make_option('--password',
                    action='store',
                    help='Password for fedora user,  password=  will prompt for password'),
        )


    
    def handle(self, *args, **options):
        #counters
        counts = defaultdict(int)

        # check required options
        if not options['username']:
            raise CommandError('Username is required')
        else:
            if not options['password'] or options['password'] == '':
                options['password'] = getpass()

        #connection to repository
        repo = Repository(username=options['username'], password=options['password'])

        try:
            #if pids specified, use that list
            if len(args) != 0:
                pids = list(args)
                pid_set = [repo.get_object(pid=p, type=AudioObject) for p in pids]

            else:
                #search for Articles
                pid_set = repo.get_objects_with_cmodel(AudioObject.AUDIO_CONTENT_MODEL, AudioObject)

        except Exception as e:
            raise CommandError('Error gettings pids (%s)' % e.message)

        try:
            objects = Paginator(pid_set, 20)
            counts['total'] = objects.count
        except Exception as e:
            self.output("Error paginating items: : %s " % (e.message))

        #process all Objects
        for p in objects.page_range:
            try:
                objs = objects.page(p).object_list
            except Exception as e:
                #print error and go to next iteration of loop
                self.output("Error getting page: %s : %s " % (p, e.message))
                counts['errors'] +=1
                continue
            for a in objs:
                try:
                    if not a.exists:
                        self.output("Skipping %s because pid does not exist" % a.pid)
                        counts['skipped'] +=1
                        continue
                    else:
                        self.output("Processing %s" % a.pid)

                        a._update_dc()

                        # save object
                        if not options['noact']:
                            a.save("cleanup DC")
                            self.output("SAVED %s" % a.pid)
                            counts['saved'] +=1
                        counts['processed'] +=1
                except Exception as e:
                    self.output("Error processing pid: %s : %s " % (a.pid, e.message))
                    counts['errors'] +=1

        # summarize what was done
        self.stdout.write("\n\n")
        self.stdout.write("Total number selected: %s\n" % counts['total'])
        self.stdout.write("Total number processed: %s\n" % counts['processed'])
        self.stdout.write("Total number saved: %s\n" % counts['saved'])
        self.stdout.write("Skipped: %s\n" % counts['skipped'])
        self.stdout.write("Errors: %s\n" % counts['errors'])


    def output(self, msg):
        self.stdout.write("%s\n" % msg)
