import sys, os, random, time, logging, getopt, signal, unicodecsv, math, urllib
from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse
from io import BytesIO
from optparse import make_option
from urlparse import urlparse
from django.conf import settings
from keep.common.fedora import Repository
from keep.common.utils import absolutize_url
from keep.arrangement.models import ArrangementObject
from keep.audio.models import AudioObject
from keep.file.models import DiskImage
from keep.video.models import Video
from eulfedora.rdfns import model as modelns
from keep.collection.models import CollectionObject
from pidservices.djangowrapper.shortcuts import DjangoPidmanRestClient
from progressbar import ProgressBar, Bar, Percentage, ETA, Counter
from eulfedora.api import ResourceIndex

class Command(BaseCommand):
    """Manage command for updating the target_uri of objects in the Pidman
       Keep domain from http to https
    """

    greetings = """
    Manage command for updating the target_uri of objects in the Pidman
    Keep domain from http to https.

    It does not regenerate the target_uri but changes the http string to
    https string in the target_uri.

    The command will also generate a summary report in which you can
    find the objects that were updated, failed to be updated, as well
    as any errors (exceptions) that may have occured.

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
        make_option('--domain',
            '-d',
            help='Override default domain defined in "settings.PIDMAN_DOMAIN"\
                  , in the format of "https://pid.library.emory.edu/domains/0/"'),
    )

    def handle(self, *args, **kwargs):
        # disable info messages in the console
        logging.getLogger('requests').setLevel(logging.CRITICAL)

        # initialize an interruption flag
        self.interrupted = False

        # initialize a Pidman client object
        self.pidman = self.get_pidman()

        # send greeting message with instructions
        self.stdout.write(self.greetings)

        # initialize dry-run flag to false
        self.is_dry_run = False

        # domain used in script
        self.query_domain = settings.PIDMAN_DOMAIN

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

        # domain from
        if kwargs.get('domain', True):
            self.query_domain = kwargs.get('domain')

        # verify environments
        environment_notice = """
        Please confirm that you would like to proceed with the
        following environments:
        PIDMAN: %s
        """ % (self.query_domain)
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
        self.summary_log.writerow(('Environments', 'PIDMAN', self.query_domain))
        self.summary_log.writerow(('Time', 'Status', 'noid', \
            'Pidman label', 'Pidman target_uri', \
            'target_uri update', 'Exception Details'))

        # collect pids in Keep Domain
        results = self.pidman.search_pids(domain_uri=self.query_domain)
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
        change_count = 0
        nochange_count = 0

        # iterate through all results fetched from pidman
        for page in range(1, pages):
            page_results = self.pidman.search_pids(domain_uri=self.query_domain, page=page)
            for page_result in page_results["results"]:
                status_label = ""
                updated_target_uri = ""
                pidman_target_uri = ""
                object_label = ""
                exception_string = ""

                try:
                    pidman_target_uri = page_result["targets"][0]["target_uri"]
                    object_label = page_result["name"]
                    target_uri = urlparse(pidman_target_uri)
                    if target_uri.scheme != "https":
                        change_count += 1
                        https_uri = "https://" + target_uri.netloc + target_uri.path
                        if not self.is_dry_run:
                            response = self.pidman.update_target(type="ark", noid=page_result["pid"], target_uri=https_uri)
                            updated_target_uri = response["target_uri"]
                            status_label = "https-changed"
                        else:
                            status_label = "updated - dry-run"
                            updated_target_uri = https_uri
                    else:
                        nochange_count += 1
                        status_label = "no-change-needed"

                except Exception as e:
                    status_label = "error"
                    exception_string += "Pidman object %s error message: %s" % (page_result["pid"], str(e))

                self.summary_log.writerow((time.strftime("%Y-%m-%d %H:%M:%S", \
                    time.localtime()), \
                    status_label, \
                    page_result["pid"], \
                    object_label, \
                    pidman_target_uri, \
                    updated_target_uri, \
                    exception_string))

                # update progress
                current_count += 1
                pbar.update(current_count)

        # update finish when all tasks are completed
        if not self.interrupted:
            pbar.finish()

        # write statistics
        self.stdout.write("Total objects: %i \n" % results_count)
        self.stdout.write("No change: %i | Change required: %i | Failed (see logs): %i\n" \
            % (nochange_count, change_count, (results_count - nochange_count - change_count)))

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
