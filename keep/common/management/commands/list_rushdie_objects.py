import sys, os, random, time, logging, getopt, signal, unicodecsv, math, urllib
from django.core.management.base import BaseCommand, CommandError
from io import BytesIO
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand
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
from eulfedora import server

class ManagementRepository(server.Repository):
    '''Convenience class to initialize an instance of :class:`eulfedora.server.Repository`
    with Fedora management/maintenance account credentials defined in Django settings.
    .. Note::
        This :class:`~eulfedora.server.Repository` variant should *only*
        be used for maintainance tasks (e.g., scripts that ingest,
        modify, or otherwise manage content).  It should **not** be
        used for general website views or access; those views should
        use the standard :class:`~eulfedora.server.Repository` which
        will pick up the default, non-privileged credentials intended
        for read and display access but not for modifying content in
        the repository.
    '''
    default_pidspace = getattr(settings, 'FEDORA_PIDSPACE', None)
    # default pidspace is not automatically pulled from django conf
    # when user/password are specified, so explicitly set it here

    def __init__(self):
        # explicitly disabling other init args, so that anyone who tries to use
        # this as a regular repo will get errors rather than confusing behavior
        super(ManagementRepository, self).__init__(username=settings.FEDORA_MANAGEMENT_USER,
                                                   password=settings.FEDORA_MANAGEMENT_PASSWORD)

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
    """

    # dry-run option declaration
    option_list = BaseCommand.option_list + (
        make_option('--update-rushdie-pidman',
            action='store_true',
            help='Dry run the command to get an output but with no changes applied'),
        )

    def handle(self, *args, **kwargs):
        # disable info messages in the console
        logging.getLogger('requests').setLevel(logging.CRITICAL)

        # initialize a Pidman client object
        self.pidman = self.get_pidman()

        # initialize a Fedora repository object
        self.repo = ManagementRepository()

        # send greeting message with instructions
        self.stdout.write(self.greetings)

        # initialize an update flag to false
        self.update = False

        # dry run notice
        if kwargs.get('update_rushdie_pidman', True):
            notice = """
            [Update Rushdie in Pidman] This will update the object title/label,
            as well as target_uri in the Rushdie Collection in Pidman

            """
            sys.stdout.write(notice)
            self.update = True

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
        self.summary_log.writerow(('Time', 'PM_Pid', 'PM_Label', 'PM_Target_URI', \
            "In_Fedora?", "Fedora_Label", "Fedora_Create_Time", "Status"))

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
                pm_object_pid, pm_object_noid, pm_label, pm_target_uri = (None,)*4
                in_fedora, fedora_object, fedora_label, fedora_create_time_stamp = (None,)*4
                status = "no-exception"

                try:
                    pm_object_pid = "emory:" + page_result["pid"]
                    pm_object_noid = page_result["pid"]
                    pm_label = page_result["name"]
                    pm_target_uri = page_result["targets"][0]["target_uri"]
                    fedora_object = self.repo.get_object(pm_object_pid)
                    import pdb; pdb.set_trace()
                    in_fedora = "Yes" if fedora_object.exists else "No"
                    fedora_label = fedora_object.label

                    # update metadata when update flag is set
                    if self.update:
                        # label update
                        if pm_label != fedora_label and fedora_label is not None:
                            self.pidman.update_pid(noid=pm_object_noid, name=fedora_label)

                        # target_uri update
                        # create the target_uri using the logic that is used in creating objects from TheKeep
                        keep_target = reverse(fedora_object.NEW_OBJECT_VIEW, kwargs={'pid': fedora_object.pid})
                        keep_target = urllib.unquote(keep_target)
                        keep_target_uri = absolutize_url(keep_target)
                        if pm_target_uri != keep_target_uri:
                            self.pidman.update_target(noid=pm_object_noid, target_uri=keep_target_uri)
                    fedora_create_time_stamp = fedora_object.created.strftime("%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    status = "Exception: %s" % str(e)

                self.summary_log.writerow((time.strftime("%Y-%m-%d %H:%M:%S", \
                    time.localtime()), \
                    pm_object_pid, \
                    pm_label, \
                    pm_target_uri, \
                    in_fedora, \
                    fedora_label, \
                    fedora_create_time_stamp, \
                    status))

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
