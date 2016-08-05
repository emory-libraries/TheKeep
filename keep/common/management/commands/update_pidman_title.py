import sys, os, random, time, logging, getopt
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand
from keep.common.fedora import Repository
from keep.arrangement.models import ArrangementObject
from keep.audio.models import AudioObject
from keep.file.models import DiskImage
from keep.video.models import Video
from eulcm.models import boda
from keep.collection.models import SimpleCollection
from keep.collection.models import CollectionObject
from pidservices.djangowrapper.shortcuts import DjangoPidmanRestClient

class Command(BaseCommand):
    """Manage command for updating the title of objects in the pidman with information
       from the Keep.
    """

    greetings = """
    This manage command will help you synchronize object titles from
    the Keep to the Pid Manager. It reads object titles from Fedora and
    compare them against those in Pidman, and update the title when
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

        # start the object collection process
        self.stdout.write("Started collecting objects from Fedora...")

        # get objects of different content models
        audio_objects = self.repo.get_objects_with_cmodel(AudioObject.AUDIO_CONTENT_MODEL)
        self.stderr.write("%i Audio objects found." % len(audio_objects))

        video_objects = self.repo.get_objects_with_cmodel(Video.VIDEO_CONTENT_MODEL)
        self.stderr.write("%i Video objects found." % len(video_objects))

        arrangement_objects = self.repo.get_objects_with_cmodel(ArrangementObject.ARRANGEMENT_CONTENT_MODEL)
        self.stderr.write("%i Arrangement objects found." % len(arrangement_objects))

        diskimage_objects = self.repo.get_objects_with_cmodel(DiskImage.DISKIMAGE_CONTENT_MODEL)
        self.stderr.write("%i DiskImage objects found." % len(diskimage_objects))

        simple_collection_objects = self.repo.get_objects_with_cmodel(SimpleCollection.COLLECTION_CONTENT_MODEL)
        self.stderr.write("%i SimpleCollection objects found." % len(simple_collection_objects))

        collection_objects = self.repo.get_objects_with_cmodel(CollectionObject.COLLECTION_CONTENT_MODEL)
        self.stderr.write("%i Collection objects found." % len(collection_objects))

        mailbox_objects = self.repo.get_objects_with_cmodel(boda.Mailbox.MAILBOX_CONTENT_MODEL)
        self.stderr.write("%i Mailbox objects found." % len(mailbox_objects))

        # end the object collection process and start
        self.stdout.write("Object collection finished.")

        # update objects in each content model
        self.update_progress(audio_objects, "AudioObject", self.pidman)
        self.update_progress(video_objects, "VideoObject", self.pidman)
        self.update_progress(arrangement_objects, "ArrangementObject", self.pidman)
        self.update_progress(diskimage_objects, "DiskImage", self.pidman)
        self.update_progress(simple_collection_objects, "SimpleCollection", self.pidman)
        self.update_progress(collection_objects, "CollectionObject", self.pidman)
        self.update_progress(mailbox_objects, "Mailbox", self.pidman)

    def update_progress(self, objects, task_name, pidman):
        """Update the objects in Pidman and reports progress back to the user.

        Args:
           objects (array): Array of objects retreived from Fedora
           task_name (str): Name of each task (object collection)
           pidman (DjangoPidmanRestClient): PidmanRestClient that can be used
            to interact with Pidman
        """
        # update progress on the screen
        sys.stdout.write("Starting %s tasks \n" % task_name)
        sys.stdout.flush()

        # initialize counters
        total_count = len(objects)
        fail_count = 0
        change_count = 0
        nochange_count = 0

        # create log files
        change_log = open(("%s/%s" % (self.output_path, "change.csv")), "w+")
        nochange_log = open(("%s/%s" % (self.output_path, "nochange.csv")), "w+")
        summary_log = open(("%s/%s" % (self.output_path, "summary.log")), "w+")

        # iterate through all items in collection
        for index, item in enumerate(objects):
            try:
                pidman_label = pidman.get_ark(item.noid)['name']
                # TODO: to be safe the actual code to update is not included here
                # will verify the environments before we accidentally start
                # a detrimental process
                # if self.is_dry_run:
                #     #TODO skip the actual update codes
                # else:
                #     #TODO actually update (BE CAREFUL)

                # when the names are not the same
                if (pidman_label != item.label):
                    change_count += 1
                    # change_log.write("[TIME]: %s, [PID]: %s, [FEDORA_LABEL]: %s, [PIDMAN_LABEL]: %s \n" % (time.strftime("%Y%m%d %H:%M:%S", time.localtime()), item.pid, item.label, pidman_label) )
                    change_log.write("%s, %s, %s, %s, %s\n" % \
                        (time.strftime("%Y-%m-%d %H:%M:%S", \
                        time.localtime()), \
                        task_name, \
                        item.pid, \
                        item.label, \
                        pidman_label))
                # when the names are the same
                else:
                    nochange_count += 1
                    # nochange_log.write("[TIME]: %s, [PID]: %s, [FEDORA_LABEL]: %s, [PIDMAN_LABEL]: %s \n" % (time.strftime("%Y%m%d %H:%M:%S", time.localtime()), item.pid, item.label, pidman_label) )
                    nochange_log.write("%s, %s, %s, %s, %s\n" % \
                        (time.strftime("%Y-%m-%d %H:%M:%S", \
                        time.localtime()), \
                        task_name, \
                        item.pid, \
                        item.label, \
                        pidman_label))

                # #TODO: remove this: write in the success log
                # success_log.write("[TIME]: %s, [PID]: %s, [FEDORA_LABEL]: %s, [PIDMAN_LABEL]: %s \n" % (time.strftime("%Y%m%d %H:%M:%S", time.localtime()), item.pid, item.label, pidman_label) )
                # success_count += 1

                # update progress on screen
                msg = "Object %i of %i for %s" % (index, len(objects)-1, task_name)
                sys.stdout.write(msg + chr(8) * len(msg))
                sys.stdout.flush()
                time.sleep(0.1)

            # when any errors (exceptions) occur
            except Exception, e:
                fail_count += 1

                # log the failure in a file
                error_file_path = "%s/%s.log" % (self.error_path, item.noid)
                error_log = open(error_file_path, 'w+')
                error_log.write('[TIME]: %s, [CONTENT_MODEL]: %s, [PID]: %s\n %s \n' % \
                    (time.strftime("%Y%m%d %H:%M:%S", time.localtime()), \
                    task_name, \
                    item.noid, \
                    str(e)))
                error_log.close()

        # update progress to "DONE" when all items are iterated through
        sys.stdout.write("DONE" + " "*len(msg)+"\n")
        sys.stdout.flush()

        # write statistics
        summary_log.write("Total objects: %i \n" % total_count)
        summary_log.write("Failed objects: %i \n" % fail_count)
        summary_log.write("No change: %i | Change required: %i\n" % (nochange_count, change_count))
        summary_log.close()

    def get_pidman(self):
        """Initialize a new Pidman client using the DjangoPidmanRestClient
        wrapper. The credentials are pulled from the application settings.

        Returns:
            DjangoPidmanRestClient

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
