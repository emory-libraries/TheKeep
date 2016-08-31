import sys, os, random, time, logging, getopt, signal, unicodecsv, math
from django.core.management.base import BaseCommand, CommandError
from io import BytesIO
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand
from keep.common.fedora import Repository
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
    """Manage command for listing Rushdie objects
    """

    greetings = """
    Rushdie colliding pid script
    """

    def handle(self, *args, **kwargs):
        # disable info messages in the console
        logging.getLogger('requests').setLevel(logging.CRITICAL)

        # initialize an interruption flag
        self.interrupted = False

        # initialize a Pidman client object
        self.pidman = self.get_pidman()

        # initialize a Fedora repository object
        self.repo = Repository()

        # send greeting message with instructions
        self.stdout.write(self.greetings)

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
        self.summary_log.writerow(('Time', 'Pid', 'Label', 'URI', 'Target URI', 'Access URI'))

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

        # bind a handler for interrupt signal
        signal.signal(signal.SIGINT, self.interrupt_handler)

        # initialize a progress bar following the Readux example
        pbar = ProgressBar(widgets=[Percentage(),
            ' (', Counter(), ')',
            Bar(),
            ETA()],
            maxval=results_count).start()

        max_results_per_page = results["max_results_per_page"]
        pages = int(math.ceil(results_count / max_results_per_page))
        current_count = 0
        for page in range(1, pages):
            page_results = self.pidman.search_pids(domain="Rushdie Collection", page=page)
            for page_result in page_results["results"]:
                object_pid = page_result["pid"]
                label = page_result["name"]
                uri = page_result["targets"][0]["uri"]
                target_uri = page_result["targets"][0]["target_uri"]
                access_uri = page_result["targets"][0]["access_uri"]
                current_count += 1
                self.summary_log.writerow((time.strftime("%Y-%m-%d %H:%M:%S", \
                    time.localtime()), \
                    object_pid, \
                    label, \
                    uri, \
                    target_uri, \
                    access_uri))

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

    def interrupt_handler(self, signum, frame):
        '''Gracefully handle a SIGINT. Stop and report what was done.
            Originally from Readux
        '''
        if signum == signal.SIGINT:
            # restore default signal handler so a second SIGINT can be used to quit
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            # set interrupt flag so main loop knows to quit
            self.interrupted = True

    def summarize_work(self, object_class, content_model_name):
        '''Summarize the number of object that is available to be processed for each
            content model type. It uses a generator to collect the total number of
            objects, prompts the user on the screen, and return the total count.

            :param object_class: the class of a object collection
            :param content_model_name: a human readable name for the content model/objects
            :type content_model: str
            :type content_model_name: str
            :return: object_count total count of objects founds within a collection
            :rtype: number
        '''
        count_query = "* <fedora-model:hasModel> <%s>" % str(object_class.CONTENT_MODELS[0])
        object_count = self.repo.risearch.count_statements(count_query)
        self.stderr.write("%i %s objects found." % (object_count, content_model_name))
        return object_count
