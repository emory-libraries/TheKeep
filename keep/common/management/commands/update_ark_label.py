import sys, os, random, time, logging, getopt, signal, unicodecsv
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
    """Manage command for updating the label of objects in the pidman with information
       from the Keep.
    """

    greetings = """
    This manage command will help you synchronize object labels from
    the Keep to the Pid Manager. It reads object labels from Fedora and
    compare them against those in Pidman, and update the label when
    there is a descrepancy.

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
    )

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
        self.summary_log.writerow(('Time', 'Status', 'Content Model', 'PID', 'Label in Fedora', 'Label in Pidman'))

        # start the object collection process
        self.stdout.write("Started summarize objects from Fedora...")

        # get object counts with Fedora ResourceIndex and summarize stats on screen
        audio_count = self.summarize_work(AudioObject, "Audio")
        video_count = self.summarize_work(Video, "Video")
        arrangement_count = self.summarize_work(ArrangementObject, "Arrangement")
        diskimage_count = self.summarize_work(DiskImage, "DiskImage")
        collection_count = self.summarize_work(CollectionObject, "Collection")

        # end the object summarization process
        self.stdout.write("Object summarization finished.")

        # update objects in each content model
        self.update_progress(AudioObject, "Audio", audio_count)
        self.update_progress(Video, "Video", video_count)
        self.update_progress(ArrangementObject, "Arrangement", arrangement_count)
        self.update_progress(DiskImage, "DiskImage", diskimage_count)
        self.update_progress(CollectionObject, "Collection", collection_count)

    def update_progress(self, object_class, content_model_name, total_count):
        """Update the objects in Pidman and reports progress back to the user.

            :param object_class: the class of a object collection
            :param content_model_name: a human readable name for the content model/objects
            :param total_count: total count of objects founds within a collection
            :type content_model: str
            :type content_model_name: str
            :type total_count: number
        """

        # initialize counters and a status label (needs change vs. does not need change)
        change_count = 0
        nochange_count = 0
        status_label = ""

        # update progress on the screen
        sys.stdout.write("Starting %s task. %i objects in total.\n" % (content_model_name, total_count))
        sys.stdout.flush()

        # bind a handler for interrupt signal
        signal.signal(signal.SIGINT, self.interrupt_handler)

        # initialize a progress bar following the Readux example
        pbar = ProgressBar(widgets=[Percentage(),
            ' (', Counter(), ')',
            Bar(),
            ETA()],
            maxval=total_count).start()

        # use generator to process each object
        object_uris = self.repo.risearch.get_subjects(modelns.hasModel, object_class.CONTENT_MODELS[0])
        for object_uri in object_uris:
            try:
                digital_object = self.repo.get_object(object_uri, object_class)
                pidman_label = self.pidman.search_pids(domain_uri=settings.PIDMAN_DOMAIN, pid=digital_object.noid)["results"][0]["name"]

                # execute irreversible update when the dry run flag is not set
                # be cautious
                if not self.is_dry_run:
                    digital_object.update_ark_label(force_update=True)

                # when the names are not the same
                if (pidman_label != digital_object.label):
                    change_count += 1
                    status_label = "change-needed"

                # when the names are the same
                else:
                    nochange_count += 1
                    status_label = "no-change-needed"

                # write to CSV
                self.summary_log.writerow((time.strftime("%Y-%m-%d %H:%M:%S", \
                    time.localtime()), \
                    status_label, \
                    content_model_name, \
                    digital_object.pid, \
                    digital_object.label, \
                    pidman_label))

            # when any errors (exceptions) occur
            except Exception, e:
                # log the failure in a file
                error_file_path = "%s/%s.log" % (self.error_path, digital_object.noid)
                error_log = open(error_file_path, 'w+')
                error_log.write('[TIME]: %s, [CONTENT_MODEL]: %s, [PID]: %s\n %s \n' % \
                    (time.strftime("%Y%m%d %H:%M:%S", time.localtime()), \
                    content_model_name, \
                    digital_object.noid, \
                    str(e)))
                error_log.close()

            # update progress
            pbar.update(change_count + nochange_count)

            # break if anything goes wrong
            if self.interrupted:
                break

        # update finish when all tasks are completed
        if not self.interrupted:
            pbar.finish()

        # write statistics
        self.stdout.write("Total objects: %i \n" % total_count)
        self.stdout.write("No change: %i | Change required: %i | Failed (see logs): %i\n" \
            % (nochange_count, change_count, (total_count - nochange_count - change_count)))

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
