from collections import defaultdict
from optparse import make_option
import re

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from eulfedora.rdfns import relsext, model as modelns
from pidservices.djangowrapper.shortcuts import DjangoPidmanRestClient

from keep.arrangement.models import ArrangementObject
from keep.collection.models import SimpleCollection as ProcessingBatch
from keep.common.fedora import Repository


class Command(BaseCommand):
    help = '''
'''
    args = '<batch id>'
    option_list = BaseCommand.option_list + (
        make_option('-n', '--noact', action='store_true', default=False,
                    help='''Test run: report what would be done, but do not modify
                    anything in the repository'''),
        )
    # default django verbosity levels: 0 = none, 1 = normal, 2 = all
    v_normal = 1

    # email folder names for 5300c
    email_folders = ('In', 'Out', 'Old-In', 'Old-Out')
    'known email folders on the 5300c, for identifying current records'
    email_path_regex = '^(%s)/' % '|'.join(email_folders)

    unused_pid_name = 'rushdie 5300c email message (unused)'
    'place-holder PID value for deactivated pids, to identify for re-use'
    unused_pid_url = 'http://rushdie.5300c.email.message/unused'
    # bogus place-holder target url for deactivated pids; this is a
    # bit of a cheat so we can find the pids easily, because pidman
    # REST API currently does not support searching by name

    def handle(self, batch_id=None, verbosity=1, noact=False, *args, **options):

        # check batch object
        if batch_id is None:
            raise CommandError('Processing batch id is required')
        self.verbosity = int(verbosity)  # ensure we compare int to int
        
        repo = Repository()
        batch = repo.get_object(batch_id, type=ProcessingBatch)
        if not batch.exists:
            raise CommandError('Processing batch %s not found' % batch_id)
        print 'Looking for email messages in processing batch "%s"' \
              % batch.label

        try:
            pidman = DjangoPidmanRestClient()
        except:
            raise CommandError('Error initializing PID manager client; ' +
                               'please check settings.')

        # iterate over all items that are part of this batch
        items = list(batch.rels_ext.content.objects(batch.uriref,
                                                    relsext.hasMember))
        
        stats = defaultdict(int)
        
        for i in items:
            # for now, init as arrangement objects 
            obj = repo.get_object(str(i), type=ArrangementObject)
            # NOTE: in dev/test, collection currently references all items
            # but only a handful actually exist in dev/test repo; just skip 
            if not obj.exists:
                continue

            # number of objects
            stats['count'] += 1

            if not obj.filetech.exists or not obj.filetech.content.file:
                print 'Error: no file tech for %s; skipping' % obj.pid
                continue

            # 5300c email messages should only have one file path.
            # Identify email messages by file path starting with
            # email folder name and  no checksum
            file_info = obj.filetech.content.file[0]
            if re.match(self.email_path_regex, file_info.path) and \
               not file_info.md5:
                print '%s is an email message' % obj.pid
                stats['email'] += 1

                if not noact:
                    try:
                        # update ark name/domain
                        pidman.update_ark(obj.noid,
                                          name=self.unused_pid_name,
                                          domain=settings.PIDMAN_DOMAIN)
                        # mark default target as inactive
                        pidman.update_ark_target(obj.noid, active=False,
                                                 target_uri=self.unused_pid_url)
                        stats['pids'] +=1
                        if self.verbosity > self.v_normal:
                            print 'Updated ARK for %s' % obj.noid

                        # reinit client as a workaround for pidman errors (?)
                        pidman = DjangoPidmanRestClient()                            
                    except Exception as e:
                        print 'Error updating ARK for %s: %s' % \
                              (obj.noid, e)

                    # purge record
                    repo.purge_object(obj.pid,
                                      'removing metadata arrangement 5300c email record')
                    stats['purged'] += 1
                    if self.verbosity > self.v_normal:
                            print 'Purged %s' % obj.pid

                    # TODO: error handling


        # summary
        if self.verbosity >= self.v_normal:
            print '''\nChecked %(count)d records, found %(email)d emails''' % stats
            if not noact:
                print 'Updated %(pids)d ARK(s); purged %(purged)d objects' \
                      % stats
