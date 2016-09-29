import sys, os, random, time, logging, getopt, signal, unicodecsv, math, urllib
from django.core.urlresolvers import reverse
from django.core.management.base import BaseCommand, CommandError
from io import BytesIO
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand
from keep.common.utils import absolutize_url
from keep.common.fedora import ManagementRepository
from keep.arrangement.models import ArrangementObject
from keep.audio.models import AudioObject
from keep.file.models import DiskImage
from keep.video.models import Video
from eulfedora.rdfns import model as modelns
from eulfedora.server import TypeInferringRepository
from keep.collection.models import CollectionObject
from pidservices.djangowrapper.shortcuts import DjangoPidmanRestClient
from progressbar import ProgressBar, Bar, Percentage, ETA, Counter
from eulfedora.api import ResourceIndex
from eulfedora import server


class Command(BaseCommand):
    """Manage command for listing Rushdie objects
    """

    greetings = """
    Rushdie colliding pid script.
    It fetches all pid objects from domain "Rushdie Collection"
    and looks up corresponding pids in Fedora to see if they exist.
    Whether it exsits in Fedora or not it will genereate a report that summarizes
    the findings.

    Before you run please make sure you have the correct credentials for Pidman
    and Fedora environments so that you are getting results of what you are concerned about.

    Dry run is an option that only generates the report without applying
    any changes. Please be sure that you know what you are doing, and
    have the Fedora and Pidman environments set up correctly before
    you proceed. You can use '-n' or '--dry-run' to enable the dry run
    mode.
    """

    # dry-run option declaration
    option_list = BaseCommand.option_list + (
        make_option('--dry-run',
            '-n',
            action='store_true',
            help='Dry run the command to get an output but with no changes applied'),
    )

    def handle(self, *args, **kwargs):
        # disable info messages in the console
        logging.getLogger('requests').setLevel(logging.CRITICAL)

        # initialize a Pidman client object
        self.pidman = self.get_pidman()

        # initialize a TypeInferringRepository object
        self.repo = TypeInferringRepository(username=settings.FEDORA_MANAGEMENT_USER, password=settings.FEDORA_MANAGEMENT_PASSWORD)

        # send greeting message with instructions
        self.stdout.write(self.greetings)

        # initialize dry-run flag to false
        self.is_dry_run = False

        # dry run notice
        if kwargs.get('dry_run', True):
            dry_run_notice = """
            [DRY-RUN ACTIVATED] Currently you are running the script
            in dry-run mode. It means that no changes will be applied
            to any of the repositories except for that the script will
            still generate statistics about objects in your repositories.

            """
            sys.stdout.write(dry_run_notice)
            self.is_dry_run = True

        # verify environments
        environment_notice = """
        Please confirm that you would like to proceed with the
        following environments:
        FEDORA: %s
        PIDMAN: %s
        """ % (settings.FEDORA_ROOT, settings.PIDMAN_DOMAIN)
        self.stdout.write(environment_notice)

        # confirm to proceed
        confirmation = raw_input("Verify above information and type 'yes' to proceed: ")
        if (confirmation != "yes"):
            self.stdout.write("Answer is not 'yes'. Operation aborted.")
            sys.exit(1)

        # setup output directory paths
        self.current_time_string = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        self.output_path = "%s/%s/%s/" % (os.getcwd(), "tmp", self.current_time_string)
        self.error_path = "%s/errors/" % self.output_path

        # create output directories
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        if not os.path.exists(self.error_path):
            os.makedirs(self.error_path)

        # create log files
        summary_log_path = open("%s/%s" % (self.output_path, "summary.csv"), 'wb')
        self.summary_log = unicodecsv.writer(summary_log_path, encoding='utf-8')
        self.summary_log.writerow(('Environments', 'FEDORA', settings.FEDORA_ROOT, 'PIDMAN', settings.PIDMAN_DOMAIN))
        self.summary_log.writerow(('Time', 'Status', 'PM_Pid', 'PM_Label', 'PM_Target_URI', 'Supposed_Label', 'Supposed_Target_URI', \
            "In_Fedora?", "Fedora_Label", "Fedora_Create_Time", "Exceptions"))

        # collect pids in Rushdie Collection
        results = self.pidman.search_pids(domain="Rushdie Collection")
        results_count = results["results_count"]

        self.update_progress(results, results_count)

    def update_progress(self, results, results_count):
        """Report the objects in Pidman and summarize in a CSV.

            :param results: results from pidman
            :param results_count: total count of objects founds within a collection
        """

        # update progress on the screen
        sys.stdout.write("%i objects in total.\n" % results_count)
        sys.stdout.flush()

        # initialize a progress bar following the Readux example
        pbar = ProgressBar(widgets=[Percentage(),
            ' (', Counter(), ')',
            Bar(),
            ETA()],
            maxval=results_count).start()

        max_results_per_page = results["max_results_per_page"]
        pages = int(math.ceil(results_count / float(max_results_per_page))) + 1
        current_count = 0

        # iterate through all results fetched from pidman
        for page in range(1, pages):
            page_results = self.pidman.search_pids(domain="Rushdie Collection", page=page)
            for page_result in page_results["results"]:
                pm_object_pid, pm_object_noid, pm_label, updated_pm_label, pm_target_uri = (None,)*5
                in_fedora, fedora_object, fedora_label, fedora_create_time_stamp = (None,)*4
                supposed_label, supposed_target_uri = (None,)*2
                status_label = "dry-run"
                exception_label = "no-exception"

                try:
                    pm_object_pid = "emory:" + page_result["pid"]
                    pm_object_noid = page_result["pid"]
                    pm_label = page_result["name"]
                    pm_target_uri = page_result["targets"][0]["target_uri"]
                    fedora_object = self.repo.get_object(pm_object_pid)
                    in_fedora = True if fedora_object.exists else False


                    status_label = "actual-run"
                    # fedora object doesn't exist:
                    # - mark item as PIDMAN_RUSHDIE_UNUSED_URI
                    # - use generic target URI PIDMAN_RUSHDIE_UNUSED_URI
                    # - set status_label as "unused-pid-identified"
                    if not fedora_object.exists:
                        if not self.is_dry_run:
                            status_label = "actual-run"
                            pid_response = self.pidman.update_pid(type="ark", noid=pm_object_noid, name=settings.PIDMAN_RUSHDIE_UNUSED)
                            target_response = self.pidman.update_target(type="ark", noid=pm_object_noid, target_uri=settings.PIDMAN_RUSHDIE_UNUSED_URI)
                            if pid_response["name"] == settings.PIDMAN_RUSHDIE_UNUSED and target_response["target_uri"] == settings.PIDMAN_RUSHDIE_UNUSED_URI:
                                status_label += ", unused-pid-updated"
                            else:
                                status_label += ", unused-pid-update-failed"
                        else:
                            supposed_label = settings.PIDMAN_RUSHDIE_UNUSED
                            supposed_target_uri = settings.PIDMAN_RUSHDIE_UNUSED_URI

                    # fedora object exists
                    # - update label to that in Fedora
                    # - update target_uri to that in Fedora
                    else:
                        if not self.is_dry_run:
                            # label update
                            fedora_label = fedora_object.label
                            if pm_label != fedora_label and fedora_label is not None:
                                response = self.pidman.update_pid(type="ark", noid=pm_object_noid, name=fedora_label)
                                if response["name"] == fedora_label:
                                    status_label += ", label-updated"
                                else:
                                    status_label += ", label-update-failed"

                            # target_uri update
                            # create the target_uri using the logic that is used in creating objects from TheKeep
                            keep_target = reverse(fedora_object.NEW_OBJECT_VIEW, kwargs={'pid': fedora_object.pid})
                            keep_target = urllib.unquote(keep_target)
                            keep_target_uri = absolutize_url(keep_target)
                            if pm_target_uri != keep_target_uri:
                                response = self.pidman.update_target(type="ark", noid=pm_object_noid, target_uri=keep_target_uri)
                                if keep_target_uri == response["target_uri"]:
                                    status_label += ", target_uri-updated"
                                else:
                                    status_label += ", target_uri-update-failed"
                        else:
                            keep_target = reverse(fedora_object.NEW_OBJECT_VIEW, kwargs={'pid': fedora_object.pid})
                            keep_target = urllib.unquote(keep_target)
                            supposed_label = fedora_object.label
                            supposed_target_uri = absolutize_url(keep_target)

                    fedora_create_time_stamp = fedora_object.created.strftime("%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    exception_label = "Exception: %s" % str(e)

                self.summary_log.writerow((time.strftime("%Y-%m-%d %H:%M:%S", \
                    time.localtime()), \
                    status_label, \
                    pm_object_pid, \
                    pm_label, \
                    pm_target_uri, \
                    supposed_label, \
                    supposed_target_uri, \
                    str(in_fedora), \
                    fedora_label, \
                    fedora_create_time_stamp, \
                    exception_label))

                current_count += 1

                # update progress
                pbar.update(current_count)

    def get_pidman(self):
        """Initialize a new Pidman client using the DjangoPidmanRestClient
            wrapper. The credentials are pulled from the application settings.

            :return: a Pidman client to interact with the Pidman APIs
            :rtype: DjangoPidmanRestClient

        """
        # try to configure a pidman client to get pids.
        try:
            return DjangoPidmanRestClient()
        except CommandError as e:
            error_msg = """
            Cannot initialize DjangoPidmanRestClient.
            Please check your configuration for more details.
            """
            sys.stderr.write(error_msg)
            raise CommandError(e)
