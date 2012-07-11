import codecs
from collections import defaultdict
import hashlib
import email
from optparse import make_option
import os
import re

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse

from bodatools.binfile import eudora
from eulfedora.rdfns import relsext, model as modelns
from eulfedora.util import RequestFailed
from eulxml.xmlmap import mods, cerp
from pidservices.clients import parse_ark
from pidservices.djangowrapper.shortcuts import DjangoPidmanRestClient

from keep.arrangement.models import ArrangementObject, RushdieArrangementFile, \
     EmailMessage, Mailbox
from keep.collection.models import SimpleCollection as ProcessingBatch
from keep.common.fedora import Repository, ArkPidDigitalObject
from keep.common.models import rights_access_terms_dict
from keep.common.utils import md5sum, solr_interface, absolutize_url


# NOTE: this is *not* in svn because it contains sensitive info
# to be redacted email messages
from email_redactions import redactions
# content should look something like this:
# redactions = {
#    r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}': 'IP address',
# }
#    regex to replace : label to display (i.e., [REDACTED: IP address])


UNUSED_PID_NAME = 'rushdie 5300c email message (unused)'
'place-holder PID value for deactivated pids, to identify for re-use'
UNUSED_PID_URL = 'http://rushdie.5300c.email.message/unused'
# bogus place-holder target url for deactivated pids; this is a
# bit of a cheat so we can find the pids easily, because pidman
# REST API currently does not support searching by name



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
        make_option('-m', '--max', metavar='MAX_NUM', dest='max_ingest', type='int',
                    help='''Stop after ingesting MAX_NUM items'''),
        make_option('--skip-purge', action='store_true', default=False,
                    help='''Skip purging old metadata email records and only
                    ingest email messages (e.g., if purge has already been completed)'''),

        make_option('--purge-only', action='store_true', default=False,
                    help='''Only purge old metadata email records; do not 
                    ingest email messages'''),

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

    max_ingest = None

    def handle(self, batch_id=None, folder_path=None, verbosity=1, noact=False,
               max_ingest=None, skip_purge=False, purge_only=False, *args, **options):

        # check batch object
        if batch_id is None:
            raise CommandError('Processing batch id is required')
        self.verbosity = int(verbosity)  # ensure we compare int to int
        if max_ingest is not None:
            self.max_ingest = int(max_ingest)

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
        # purge old metadata email 'arrangement' objects that belong to this batch
        if not skip_purge:
            self.remove_arrangement_emails(batch)
        # ingest new objects for email mailboxes & messages
        if not purge_only:
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
                # reinit client as a workaround for pidman errors (?)
                pidman = DjangoPidmanRestClient()
                # update ark name/domain
                pidman.update_ark(obj.noid,
                                  name=UNUSED_PID_NAME,
                                  domain=settings.PIDMAN_DOMAIN)
                # mark default target as inactive
                pidman.update_ark_target(obj.noid, active=False,
                                         target_uri=UNUSED_PID_URL)
                self.stats['pids'] +=1
                if self.verbosity > self.v_normal:
                    print 'Updated ARK for %s' % obj.noid
                    
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
            self.stats['folder'] += 1

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
                    
                mailbox = self.repo.get_object(type=MailboxPidReuse)
                desc = 'Rushdie\'s email from his PowerBook 5300c: "%s" folder' % \
                       folder_name 
                mailbox.label = desc
                mailbox.dc.content.title = desc
                # mailbox should belong to same collection mailbox files do
                if mbox_obj.collection:
                    mailbox.collection = mbox_obj.collection
                elif mbox_obj._deprecated_collection:
                    mailbox.collection = mbox_obj._deprecated_collection
                
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

                # NOTE: should be able to get rushdie collection
                # object from toc/mbox objects, but they seem to have
                # isMemberOf rel instead of isMemberOfCollection (?)
            else:
                # FIXME: boda rel is giving us boda mailbox instead of local
                # arrangement mailbox; re-init as local mailbox
                # for access to parent collection
                mailbox = self.repo.get_object(mailbox.pid, type=MailboxPidReuse)
                
                

            with open(folder_toc) as tocdata:
                with open(folder_path) as mbox:
                    toc = eudora.Toc(tocdata)   # load as eudora toc binfile

                    # eudora Toc returns messages in folder order;
                    # pass order in to store in CERP for sorting/display
                    folder_order = 0
                    for msg in toc.messages:
                        self.stats['message'] += 1
                        
                        # get data from mbox file based on msg offset/size
                        mbox.seek(msg.offset)
                        # read message content from mailbox data file
                        msg_data = mbox.read(msg.size)
                        
                        self.ingest_message(msg_data, mailbox, folder_order)
                        folder_order += 1
                        # max to ingest for testing
                        if self.max_ingest and self.stats['ingested'] >= self.max_ingest:
                            break

        # summary

        if self.verbosity >= self.v_normal:
            print '''\nProcessed %(folder)d mail folders and %(message)d messages; %(previously_ingested)d messages previously ingested'''  % self.stats
            if not self.noact:
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


    def redact_email(self, content):
        '''Replace any sensitive information in the email message with
        a redacted text label.
        '''
        for regex, label in redactions.iteritems():
            content = re.sub(regex, '[REDACTED: %s]' % label, content,
                         flags=re.MULTILINE | re.IGNORECASE)
        return content


    def ingest_message(self, msg_data, mailbox, folder_order):

        # read content and redact IP addresses / email addresses
        msg_data = self.redact_email(msg_data)
                                        
        # generate email object from data
        email_msg = email.message_from_string(msg_data,
                                              _class=MacEncodedMessage)

        # check and warn if email has attachments
        attachments = self.email_attachments(email_msg)
        if attachments:
            print 'Warning! Email has attachments (not yet handled): %s' % \
                  ','.join(attachments)
        
        # get current content type to preserve the original value,
        # and also to determine how to decode
        content_type = email_msg.get('Content-Type', '')
        orig_content_type = email_msg.get_content_type()
        orig_content_charset = email_msg.get_content_charset()

        # at least one email in this set has a charset of 'unknown-8bit',
        # but the \xa0 in the content indicates it is probably latin 1
        if 'charset=unknown-8bit' in content_type:
            latin1_charset = email.charset.Charset('latin_1')
            email_msg.set_charset(latin1_charset)

        # otherwise, if charset is not set, assume mac roman
        elif not email_msg.get_charset():
            # tell email that charset should be mac roman,
            # so it can decode special characters
            mac_charset = email.charset.Charset('mac_roman')
            email_msg.set_charset(mac_charset)
            # decode headers from mac roman charset
            # (some messages contain improperly formatted
            # accented characters in a from/to header)
            email_msg.decode_headers() 

        # create a new object to populate with data
        msg_obj = self.repo.get_object(type=EmailMessagePidReuse)

        # generate cerp from mime message
        # - store folder order as message local id 
        msg_obj.cerp.content = cerp.Message.from_email_message(email_msg,
                                                               local_id=folder_order)

        # The generated CERP may have modified mac roman charset headers
        # which were needed to convert instead of the original;
        # update thex ml to store the original value,  NOT the encoding
        # that was used to decode the content.
        if content_type:
            if msg_obj.cerp.content.single_body:
                msg_obj.cerp.content.single_body.content_type_list[0] = orig_content_type
                msg_obj.cerp.content.single_body.charset_list[0] = orig_content_charset

        else:
            if msg_obj.cerp.content.single_body:
                del msg_obj.cerp.content.single_body.content_type_list[0]
                del msg_obj.cerp.content.single_body.charset_list[0]
        # loop through headers to set/remove content type
        for h in msg_obj.cerp.content.headers:
            if h.name == 'Content-Type':
                if content_type:
                    h.value = content_type
                else:
                    h.value = None
                    h.name = None
                break

        # construct an object label based on from/to/date/subject
        msg_from = email_msg['From']
        # NOTE: it would be nice to suppress redundant redaction email text here;
        # at least simplify label for rushdie, since that is what we'll see most
        if 'REDACTED: Salman Rushdie\'s email' in msg_from:
            msg_from = 'Salman Rushdie'
        label = u'Email from %s' %  msg_from
        if email_msg.get('To', None):
            # FIXME: could have multiple recipients
            # we *should* be able to get split-out version from email.Message ...
            to = email_msg['To']
            label += u' to %s' % email_msg['To']
        # date/subject not always present, but add if they are
        if email_msg.get('Date', None):
            label += u' on %s' % email_msg['Date']
        if email_msg.get('Subject', None):
            label += u' %s' % email_msg['Subject']            

        # set as object label and dc:title
        msg_obj.label = label
        msg_obj.dc.content.title = label

        # in verbose noact mode, print label so user can see what is being done
        if self.verbosity > self.v_normal and self.noact:
            print label

        # generate a pristine email Message for saving fedora
        # (don't save modified charset, content type, etc.)
        msg_obj.mime_data.content = email.message_from_string(msg_data,
                                              _class=MacEncodedMessage)
        # calculate an MD5 of the email content *as it will be serialized*
        md5 = hashlib.md5()
        md5.update(str(msg_obj.mime_data.content))
        email_md5 = md5.hexdigest()
        msg_obj.mime_data.checksum = email_md5


        # check if this email has already been ingested via checksum;
        # don't re-ingest if it is already in the repository
        solr = solr_interface()
        q = solr.query(content_md5=msg_obj.mime_data.checksum).field_limit('pid')
        if len(q):
            if self.verbosity >= self.v_normal:
                print 'Email message has already been ingested as %s; skipping' \
                      % q[0]['pid']
            self.stats['previously_ingested'] += 1
            return
            

        # associate with current mailbox object
        msg_obj.mailbox = mailbox
        # belongs to same collection as its mailbox
        if mailbox.collection:
            msg_obj.collection = mailbox.collection
        # ingest items as accessioned/unprocessed
        msg_obj.arrangement_status = 'accessioned'
        # ingest with a default rights code of 10 "Undetermined" in rights DS
        msg_obj.rights.content.create_access_status()
        msg_obj.rights.content.access_status.code = "10"
        msg_obj.rights.content.access_status.text = rights_access_terms_dict["10"].text
        
        if not self.noact:
            msg_obj.save('ingesting email message from rushdie 5300c')
            if self.verbosity >= self.v_normal:
                print 'Ingested message %s : %s' % \
                      (msg_obj.pid, msg_obj.label)
                self.stats['ingested'] += 1


    def email_attachments(self, msg):
        attachments = []
        if msg.is_multipart():
            payload = msg.get_payload()
            # NOTE: sub parts could themselves be multipart...
            for p in payload:
                if 'attachment' in p.get('Content-Disposition', '') \
                       or p.get_filename():
                    attachments.append(p.get_filename())

        return attachments


        

class MacEncodedMessage(email.message.Message):

    charset_decoder = codecs.getdecoder('macroman')

    def decode_headers(self):
        new_headers = []
        
        for key, val in self._headers:
            val, length = self.charset_decoder(val)
            new_headers.append((key, val))

        self._headers = new_headers




class PidReuseDigitalObject(ArkPidDigitalObject):

    _unused_pid_result = None

    def get_default_pid(self):
        if not self._unused_pid_result:
            pidman = DjangoPidmanRestClient()
            result = pidman.search_pids(target=UNUSED_PID_URL)
            # if any were found, use results
            if result and result['results_count']:
                self._unused_pid_result = result['results']

        # if we have any unused pids, pop one off and use it
        if self._unused_pid_result:
            pid_info = self._unused_pid_result.pop()
            ark = pid_info['targets'][0]['access_uri']
            parsed_ark = parse_ark(ark)
            naan = parsed_ark['naan']  # name authority number
            noid = parsed_ark['noid']  # nice opaque identifier


            # use noid as basis for new pid
            pid = '%s:%s' % (self.default_pidspace, noid)
            # calculate target to new object
            target = reverse(self.NEW_OBJECT_VIEW, kwargs={'pid': pid})
            # reverse() returns a full path - absolutize so we get scheme & server also
            target = absolutize_url(target)
            # update pid ark label from object
            pidman.update_ark(noid, name=self.label)
            # update default ark target for new object url
            pidman.update_ark_target(noid, target_uri=target, active=True)
            
            # if we have a mods datastream, store the ARK as mods:identifier
            if hasattr(self, 'mods'):
                # store full uri and short-form ark
                self.mods.content.identifiers.extend([
                    mods.Identifier(type='ark', text='ark:/%s/%s' % (naan, noid)),
                    mods.Identifier(type='uri', text=ark)
                    ])

            # always add full uri ARK to dc:identifier
            self.dc.content.identifier_list.append(ark)
            
            # use the noid to construct a pid in the configured pidspace
            return '%s:%s' % (self.default_pidspace, noid)
        
        else:
            # if we run out of pids re-use, fall back to default behavior
            return super(PidReuseDigitalObject, self).get_default_pid()

    


# extend standard mailbox/email objects to get pid re-use behavior

class MailboxPidReuse(Mailbox, PidReuseDigitalObject):
    pass

class EmailMessagePidReuse(EmailMessage, PidReuseDigitalObject):
    pass
