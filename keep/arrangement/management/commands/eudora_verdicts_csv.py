import logging
from bodatools.binfile import eudora
import csv
from datetime import datetime
import email
import hashlib
import re
from keep.common.utils import redact_email


from django.core.management.base import BaseCommand, CommandError


logger = logging.getLogger(__name__)


def get_date(msg):
    '''
    Had do get the date the hard way.
    Could not find a good way to get
    the date consistently from all the mboxes.
    Takes message_obj
    '''
    date = str(msg)
    p=re.compile('From \?\?\?\@\?\?\? (.*)') #This bit can not be accessed like a normal header for some reason.
    m = p.search(date)
    date_str =  m.group(1)
    dt = datetime.strptime(date_str, '%a %b %d %H:%M:%S %Y')
    date_formated = dt.strftime('%Y-%m-%d %H:%M:%S')
    return date_formated



class Command(BaseCommand):
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
    args = "<path to directory containing mailbox and toc files>"
    


    def handle(self, *args, **options):
        verdicts = {
            'needs-review' : 4,
            'family-corr' : 4,
            'rushdie-restrict' : 4,
            'restricted-marbl' : 4,
            'rushdie-approve': 2,
            'in': 2,
            'out': 2,
            'old-in': 2,
            'old-out': 2,

        }

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
            'SIZE'
        ]

        if len(args) == 0:
            raise CommandError("Directory containing mailbox and toc files must be specified")

        else:
            path = args[0]

        #output CSV file
        with open('email.csv', 'wb') as f:
            writer = csv.DictWriter(f, fieldnames =headers, quoting=csv.QUOTE_ALL)

            #write header row
            writer.writeheader()



            for fname in verdicts.keys():
                print "processing %s" % fname
                mbox = open(path+"/"+fname)
                toc = eudora.Toc(path+"/"+fname + '.toc')

                for i, message in enumerate(toc.messages):

                    #get message from toc
                    mbox.seek(message.offset)
                    message_data = mbox.read(message.size)
                    message_data = redact_email(message_data)
                    message_obj = email.message_from_string(message_data)

                    #get fields
                    mail_id = message_obj.get('message-id')
                    subject = message_obj.get('subject')
                    verdict = verdicts[fname]
                    date_created = get_date(message_obj)
                    computer = '5300c'
                    size = message.size
                    #md5sum
                    md5sum = hashlib.md5()
                    md5sum.update(str(message_obj))

                    #Dictwriter will keep the columns in the correct order based on headers list
                    row = {'ID': mail_id,
                       "FOLDER-SUBJECT": "%s/%s" % (fname, subject),
                       'VERDICT': verdict,
                       'CREATED': date_created,
                       'COMPUTER': computer,
                       'SIZE': size,
                       'SERIES': 'Correspondence - Email',
                       'VERDICT': verdict,
                       'CHECKSUM': md5sum.hexdigest()
                    }

                    #write row
                    writer.writerow(row)