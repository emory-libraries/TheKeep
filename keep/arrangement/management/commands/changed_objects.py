from eulcm.models import boda
from eulfedora.server import TypeInferringRepository
import logging
from optparse import make_option
from django.utils.encoding import smart_str
from django.conf import settings
import csv
from django.core.management.base import BaseCommand
from keep.arrangement.models import ArrangementObject
from keep.common.fedora import ManagementRepository


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    '''Export an existing arrangement object and import it with a new pid,
preserving all history, datastreams, audit trails, etc.
NOTE: should not be used except in dire need; may fail on large objects.'''
    help = __doc__

    option_list = BaseCommand.option_list + (
        make_option('--noact', '-n',
                    action='store_true',
                    default=False,
                    help='Quering changed objects'),
        )
        

    def handle(self, *args, **options):

        # use type-inferring repository
        repo = TypeInferringRepository(username=settings.FEDORA_MANAGEMENT_USER,
                                       password=settings.FEDORA_MANAGEMENT_PASSWORD)

        f = open("changed_objects.csv", 'wb')
        writer = csv.writer(f)
        writer.writerow([
            smart_str(u"PID"),

        ])

        # get all object that arrangements
        pid_set = repo.get_objects_with_cmodel(boda.Arrangement.ARRANGEMENT_CONTENT_MODEL, type=ArrangementObject)
        self.output(0, "Processing PIDs %s " % len(pid_set))
        for idx, item in enumerate(pid_set):
            self.output(0, "Processing PID %s " % item.pid)
            self.output(0, "Processing PID # %s " % idx)
            audit_trail = item.audit_trail
            pos_record = 0
            for record in audit_trail.records:
                if record.message != 'datastream fixity check':
                    if record.date.strftime("%Y-%m-%dT%H:%M:%S") < '2016-10-13T00:00:00' and record.date.strftime("%Y-%m-%dT%H:%M:%S") > '2016-10-03T00:00:00':
                        pos_record = pos_record + 1

            if pos_record > 0:
                writer.writerow([
                            smart_str(item.pid if item.pid else ''),

                        ])
                self.output(0, "Adding this pid %s " % item.pid)



        f.close()

    def output(self, v, msg):
        '''simple function to handle logging output based on verbosity'''
        self.stdout.write("%s\n" % msg)


