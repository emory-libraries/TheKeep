from collections import defaultdict
import email
from optparse import make_option
import os
import re

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from bodatools.binfile import eudora
from eulfedora.rdfns import relsext, model as modelns
from pidservices.djangowrapper.shortcuts import DjangoPidmanRestClient

from keep.arrangement.models import ArrangementObject
from keep.collection.models import SimpleCollection as ProcessingBatch
from keep.common.fedora import Repository


class Command(BaseCommand):
    help = '''Remove outdated email message metadata objects from the repository
and replace them with email folder and message objects based on 5300c
Eudora files. (One-time import for 5300c content)

   <batch id> pid for the 5300c processing batch object (used to find
	email records to be removed/replaced)

   <eudora base path>   base path for Eudora folder data and index files

'''
    args = '<batch id> <eudora base path>'
    option_list = BaseCommand.option_list + (
        make_option('-n', '--noact', action='store_true', default=False,
                    help='''Test run: report what would be done, but do not modify
                    anything in the repository'''),
        )
    # default django verbosity levels: 0 = none, 1 = normal, 2 = all
    v_normal = 1

    # email folder names for 5300c
    # key is fake 'path' in arrangement objects; value is original filename
    email_folders = {
        'In': 'In',
        'Out': 'Out',
        'Old-In': 'OLD "IN"',
        'Old-Out': 'OLD "OUT"',
    }
    'known email folders on the 5300c, for identifying current records'
    email_path_regex = '^(%s)/' % '|'.join(email_folders.keys())

    unused_pid_name = 'rushdie 5300c email message (unused)'
    'place-holder PID value for deactivated pids, to identify for re-use'
    unused_pid_url = 'http://rushdie.5300c.email.message/unused'
    # bogus place-holder target url for deactivated pids; this is a
    # bit of a cheat so we can find the pids easily, because pidman
    # REST API currently does not support searching by name

    def handle(self, batch_id=None, folder_path=None, verbosity=1, noact=False, *args, **options):

        # check batch object
        if batch_id is None:
            raise CommandError('Processing batch id is required')
        self.verbosity = int(verbosity)  # ensure we compare int to int

        # check folder path
        if folder_path is None:
            raise CommandError('Eudora folder base path is required')
        if not os.path.isdir(folder_path):
            raise CommandError('Eudora folder path "%s" is not a directory' % folder_path)
        self.noact = noact
        
        self.repo = Repository()
        batch = self.repo.get_object(batch_id, type=ProcessingBatch)
        if not batch.exists:
            raise CommandError('Processing batch %s not found' % batch_id)
        print 'Looking for email messages in processing batch "%s"' \
              % batch.label

        try:
            pidman = DjangoPidmanRestClient()
        except:
            raise CommandError('Error initializing PID manager client; ' +
                               'please check settings.')

        self.stats = defaultdict(int)
        # purge bogus email 'arrangement' objects that belong to this batch
        self.remove_arrangement_emails(batch)
        self.ingest_email(folder_path)


    def remove_arrangement_emails(self, batch):
        '''Find and iterate over all items that are part of the specified batch.
        Purge email message objects and update the correspending ARK records
        for re-use on ingest.
        '''
        items = list(batch.rels_ext.content.objects(batch.uriref,
                                                    relsext.hasMember))
        for i in items:
            # for now, init as arrangement objects 
            obj = self.repo.get_object(str(i), type=ArrangementObject)
            # NOTE: in dev/test, collection currently references all items
            # but only a handful actually exist in dev/test repo; just skip 
            if not obj.exists:
                continue

            # number of objects
            self.stats['count'] += 1

            if not obj.filetech.exists or not obj.filetech.content.file:
                print 'Error: no file tech for %s; skipping' % obj.pid
                continue

            # 5300c email messages should only have one file path.
            # Identify email messages by file path starting with
            # email folder name and  no checksum
            file_info = obj.filetech.content.file[0]
            if not re.match(self.email_path_regex, file_info.path) or \
               file_info.md5:
                # not an email message - skip to next item
                continue

            self.stats['email'] += 1

            # if in no-act mode, nothing else to do
            if self.noact:
                continue

            # not in no-act mode : update pid, purge object
            try:
                # update ark name/domain
                pidman.update_ark(obj.noid,
                                  name=self.unused_pid_name,
                                  domain=settings.PIDMAN_DOMAIN)
                # mark default target as inactive
                pidman.update_ark_target(obj.noid, active=False,
                                         target_uri=self.unused_pid_url)
                self.stats['pids'] +=1
                if self.verbosity > self.v_normal:
                    print 'Updated ARK for %s' % obj.noid
                    
                # reinit client as a workaround for pidman errors (?)
                pidman = DjangoPidmanRestClient()                            
            except Exception as e:
                print 'Error updating ARK for %s: %s' % \
                      (obj.noid, e)
                        
            # purge record
            try:
                self.repo.purge_object(obj.pid,
                                  'removing metadata arrangement 5300c email record')
                self.stats['purged'] += 1
                if self.verbosity > self.v_normal:
                    print 'Purged %s' % obj.pid
                            
            except RequestFailed as e:
                self.stats['purge_error'] += 1
                print 'Error purging %s: %s' % (obj.pid, e)
                        
        # summary
        if self.verbosity >= self.v_normal:
            print '''\nChecked %(count)d records, found %(email)d emails''' % self.stats
            if not self.noact:
                print 'Updated %(pids)d ARK(s); purged %(purged)d objects, error purging %(purge_error)d objects' \
                      % self.stats



    def ingest_email(self, folder_base):
        for folder_name, folder_file in self.email_folders.iteritems():
            folder_path = os.path.join(folder_base, folder_file)
            folder_toc = os.path.join(folder_base, folder_file + '.toc')
            # if either data or index file is not present, bail out
            if not os.path.isfile(folder_path) or \
                   not os.path.isfile(folder_toc):
                print 'Error: folder files %s not found at base path "%s"' % \
                      (folder_file, folder_base)
                continue

            with open(folder_toc) as tocdata, open(folder_path) as mbox:
                toc = eudora.Toc(tocdata)
                msgs = list(toc.messages)
                if self.verbosity >= self.v_normal:
                    print '%s: %d messages' % (toc.name, len(msgs))
                    
                for msg in msgs:
                    # get data from mbox file based on msg offset/size
                    msg_data = mbox.read(msg.size)
                    email_msg = email.message_from_string(msg_data)
                    print '  To %s; From %s; %s' % \
                          (email_msg['To'], email_msg['From'], email_msg.get('Subject', ''))

                
        
            # TODO: make sure to ingest as restricted / not processed
            # (don't expose anything by default or by mistake)
