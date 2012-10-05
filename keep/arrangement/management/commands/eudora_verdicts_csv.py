import csv
from datetime import datetime
import email
from glob import glob
import hashlib
import logging
import os
import re

from django.core.management.base import BaseCommand, CommandError

from bodatools.binfile import eudora
from keep.common.utils import redact_email
from keep.arrangement.management.commands.ingest_5300c_email import MacEncodedMessage

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    '''
    Generate a CSV file named emails.csv in the current directory with information
    about individual email messages from Eudora folders.  Output includes message
    checksum and a "verdict" code for setting rights information, based on the
    name of the email folder.
    '''

    # old docstring (revise/clean)
    '''
    Outputs CSV file emails.csv to current directory with info about each email message.
    The verdict and checksum are the main pieces of data generated.
    The other columns are for reference.
    The following files are used for input and
    the path to the  directory where they are located
    must be specified in the args.
    Each pair files (filename, filename.toc) maps to verdict code:

    needs-review
    needs-review.toc
    family-corr
    family-corr.toc
    rushdie-restrict
    rushdie-restrict.toc
    restricted-marbl
    restricted-marbl.toc
    rushdie-approve
    rushdie-approve.toc
    in
    in.toc
    out
    out.toc
    old-in
    old-in.toc
    old-out
    old-out.toc
    '''

    help = __doc__
    args = "<path to Eudora directory containing mailbox and toc files>"

    headers = [
        'ID',
        'CHECKSUM',
        'FOLDER-SUBJECT',
        'SERIES',
        'SUBSERIES',
        'VERDICT',
        'TYPE',
        'CREATOR',
        'ATTRIBUTES',
        'CREATED',
        'MODIFIED',
        'COMPUTER',
        'RAW SIZE',     # size of the original content from the mbox data file
        'INGEST SIZE',   # size of redacted content as it would be ingested
        'RAW DATE',  # raw date string from the message, in case it is needed for matching
    ]
    'headers for the CSV file to be generated'

    verdicts = {
        'needs review': 4,
        'family corr': 4,
        'rushdie restrict': 4,
        'restricted-marbl': 4,
        'rushdie approve': 2,
        'In': 2,
        'Out': 2,
        'OLD "IN"': 2,
        'OLD "OUT"': 2,
        "list of individuals": 4,
        "exhibitC_1": 4,
        "publishers": 4,
    }
    'mappings from folder name to numeric Keep verdict code'

    # hard-coded values to include in the CSV file for consistency
    computer = '5300c'
    'name of the computer where this content was found'
    series = 'Correspondence - Email'
    'name of the series all email content belongs to'

    def handle(self, *args, **options):

        if len(args) == 0:
            raise CommandError("Directory containing mailbox and toc files must be specified")

        else:
            eudora_path = args[0]

        # get a list of all *.toc files in the specified directory
        toc_files = glob(os.path.join(eudora_path, '*.toc'))
        if not toc_files:
            print 'Error: no *.toc files found at %s' % eudora_path
            exit(-1)

        # output CSV file
        with open('email.csv', 'wb') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers, quoting=csv.QUOTE_ALL)

            # write header row
            writer.writeheader()

            for toc_filepath in toc_files:
                fname, ext = os.path.splitext(os.path.basename(toc_filepath))

                print 'Processing \'%s\'' % fname
                # verdict is per-folder, so get it now and warn if unknown
                verdict = self.verdicts.get(fname, 'UNKNOWN')    # verdict code based on folder name
                if verdict == 'UNKNOWN':
                    print 'Warning: unknown verdict for "%s"' % fname

                # open the mailbox file as raw data
                mbox = open(os.path.join(eudora_path, fname))
                # open the toc file as a binfile eudora object
                toc = eudora.Toc(toc_filepath)

                # iterate through every email in the folder and add to csv output
                msg_count = 0
                for message in toc.messages:
                    msg_count += 1

                    # get individual message data based on size and offset from toc file
                    mbox.seek(message.offset)
                    message_data = mbox.read(message.size)
                    # redact to match content as ingested
                    message_data = redact_email(message_data)
                    # generate an email message object from the data, using the
                    # exact character encoding used for ingesting content,
                    # so that content checksums will match
                    email_msg = email.message_from_string(message_data,
                                              _class=MacEncodedMessage)

                    # get any fields that require calculation or extraction
                    raw_date, formatted_date = self.get_date(email_msg)
                    # md5sum
                    md5sum = hashlib.md5()
                    md5sum.update(str(email_msg))

                    # create a dict with the row data
                    # (order here doesn't matter since Dictwriter will write out based on headers list)
                    row = {
                        'ID': email_msg.get('message-id'),
                        'FOLDER-SUBJECT': '%s/%s' % (fname, email_msg.get('subject')),
                        'VERDICT': verdict,
                        'CREATED': formatted_date,
                        'COMPUTER': self.computer,
                        'RAW SIZE': message.size,
                        'SERIES': self.series,
                        'CHECKSUM': md5sum.hexdigest(),
                        'INGEST SIZE': len(str(email_msg)),
                        'RAW DATE': raw_date,
                    }

                    # write out the row data
                    writer.writerow(row)
                print '  %d messages' % msg_count

    def get_date(self, msg):
        '''
        Retrieve and reformat the date from an email message.

        Using a regular expression to pull from the content since
        not all emails expose the date as an actual email header for some reason.

        :returns: tuple of raw date string as found in the message, formatted date
        '''
        date = str(msg)
        # cannot be reliably accessed like a normal header
        p = re.compile('From \?\?\?\@\?\?\? (.*)')
        m = p.search(date)
        date_str = m.group(1)
        dt = datetime.strptime(date_str, '%a %b %d %H:%M:%S %Y')
        return date_str, dt.strftime('%Y-%m-%d %H:%M:%S')
