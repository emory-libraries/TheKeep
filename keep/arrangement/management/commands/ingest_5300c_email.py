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

from keep.arrangement.models import ArrangementObject, RushdieArrangementFile, \
     EmailMessage, Mailbox
from keep.collection.models import SimpleCollection as ProcessingBatch
from keep.common.fedora import Repository
from keep.common.utils import md5sum, solr_interface


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
        #TEMP self.remove_arrangement_emails(batch)
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
            
            # find the index/data file objects for this folder in fedora
            # by checksums from the originals;
            # check if they are associated with an existing mailbox object
            mailbox = None

            mbox_obj = self.find_file_object(folder_path)
            if mbox_obj is None:
                # these records should be found in production
                print 'Warning: record not found for folder data file "%s"' % folder_file
            elif mbox_obj.mailbox:
                mailbox = mbox_obj.mailbox
                    
            toc_obj = self.find_file_object(folder_toc)
            if toc_obj is None:
                print 'Warning: record not found for folder index file "%s.toc"' % folder_file
            elif toc_obj.mailbox:
                mailbox = toc_obj.mailbox

            # mailbox not found via folder file objects, so create it
            if mailbox is None:
                if self.verbosity > self.v_normal:
                    print 'Mailbox object for %s not found; creating one' % folder_name
                    
                mailbox = self.repo.get_object(type=Mailbox)
                desc = 'Rushdie\'s email from his PowerBook 5300c: "%s" folder' % \
                       folder_name 
                mailbox.label = desc
                mailbox.dc.content.title = desc
                
                # save to get a pid, add mailbox rel to file objects
                if not self.noact:
                    # TODO: fedora error handling
                    mailbox.save('email folder object for %s' % folder_name)
                    self.stats['ingested'] += 1
                    if self.verbosity >= self.v_normal:
                        print 'Created new mailbox object for %s as %s' % \
                              (folder_name, mailbox.pid)
                        
                    if mbox_obj:
                        mbox_obj.mailbox = mailbox
                        mbox_obj.save('associating with mailbox object')
                        self.stats['updated'] += 1
                    if toc_obj:
                        toc_obj.mailbox = mailbox
                        toc_obj.save('associating with mailbox object')
                        self.stats['updated'] += 1
                

            with open(folder_toc) as tocdata, open(folder_path) as mbox:
                toc = eudora.Toc(tocdata)
                for msg in toc.messages:
                    # get data from mbox file based on msg offset/size
                    mbox.seek(msg.offset)
                    msg_data = mbox.read(msg.size)
                    email_msg = email.message_from_string(msg_data)

                    msg_obj = self.repo.get_object(type=EmailMessage)

                    # NOTE: *redact* emails before creating label!

                    
                    # contstruct an email label
                    label = u'Email from %s' % unicode(email_msg['From'], errors='ignore')
                    if email_msg.get('To', None):
                        # FIXME: could have multiple recipients
                        to = unicode(email_msg['To'], errors='ignore')
                        label += u' to %s' % unicode(email_msg['To'], errors='ignore')

                    # date/subject not always present
                    if email_msg.get('Date', None):
                        label += u' on %s' % email_msg['Date']
                    if email_msg.get('Subject', None):
                        label += u' %s' % unicode(email_msg['Subject'], errors='ignore')
                        
                    msg_obj.mime_data.content = email_msg
                    msg_obj.label = label
                    msg_obj.dc.content.title = label
                    # TODO: need to set CERP

                    # TODO: check for duplicate content via checksum (?)

                    # associate with current mailbox object
                    msg_obj.mailbox = mailbox
                    if not self.noact:
                        msg_obj.save('ingesting email message from rushdie 5300c')
                        if self.verbosity >= self.v_normal:
                            print 'Ingested message %s : %s' % \
                                  (msg_obj.pid, msg_obj.label)
                        self.stats['ingested'] += 1

                    # RSK TEMP: test just ingesting one
                    break

                
        
            # TODO: make sure to ingest as restricted / not processed
            # (don't expose anything by default or by mistake)

            # TODO: created objects should all belong to parent collection
            # (i.e., rushdie archival collection)


        # summary
        if self.verbosity >= self.v_normal and not self.noact:
            print '''\nCreated %(ingested)d records, updated %(updated)d''' % self.stats



    def find_file_object(self, file_path):
        '''Find a file object by checksum in fedora based on a file
        path.  Returns a file object if one matches the checksum for
        the file specified, or else None if no match is found. 

        :returns:  :class:`keep.arrangement.models.RushdieArrangementFile` or
		None
        '''
        
        
        file_md5 = md5sum(file_path)
        solr = solr_interface()
        q = solr.query(content_md5=file_md5).field_limit('pid')
        if len(q):
            return self.repo.get_object(q[0]['pid'], type=RushdieArrangementFile)
