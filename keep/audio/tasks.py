import logging
import os
import subprocess
import tempfile
import traceback
from celery import task

from django.conf import settings
from eullocal.django.taskresult.models import TaskResult

from keep.audio.models import AudioObject, check_wav_mp3_duration
from keep.common.fedora import Repository
from keep.file.utils import md5sum

logger = logging.getLogger(__name__)


@task
def convert_wav_to_mp3(pid, use_wav=None, remove_wav=False):
    """Generate an mp3 file from a wav file associated with an
    :class:`~keep.audio.models.AudioObject`.  When conversion is successful,
    save the generated file as the compressed audio datastream of the AudioObject
    in Fedora.

    :param pid: the pid of the object to generate an MP3 for. Expected to be an
        instance of :class:`~keep.audio.models.AudioObject`.
    :param use_wav: Rather than downloading the WAV content from the fedora object,
        this will use the file path provided instead.  The file provided
        **must** match the checksum for the master audio datastream in the
        fedora object, or conversion will fail.
    :param remove_wav: If use_wav is specified, setting remove_wav to True
        will remove the file passed in when conversion task has completed.
        Optional, defaults to False.

    This function currently stores all temporary files in the ingest staging
    directory configured in django settings (to make cleanup easier, and since
    this task will normally be part of the ingest process).
    """
    try:
        #Initialize temporary file names.
        mp3_file_path = None
        wav_file_path = None

        #Initialize repo and get the object for this pid.
        repo = Repository()
        obj = repo.get_object(pid, type=AudioObject)

        # set up temp directory where file to be converted will be downloaded
        # (if necessary) and where the generated mp3 will be created
        tempdir = settings.INGEST_STAGING_TEMP_DIR
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)

        if use_wav != None:
            wav_file_path = use_wav
            mp3_file_path = wav_file_path + ".mp3"
        else:
            # download the master audio file from the object in fedora
            # mkstemp returns file descriptor and full path to the temp file
            tmpfd, wav_file_path = tempfile.mkstemp(dir=tempdir)
            mp3_file_path = wav_file_path + ".mp3"
            try:
                destination = os.fdopen(tmpfd, 'wb+')
            except Exception as e:
                logger.error("Error opening temporary file; cannot download master audio for conversion : %s" % e)
                logger.debug("Stack trace for file error:\n" + traceback.format_exc())
                os.close(tmpfd)
                raise

            try:
                destination.write(obj.audio.content.read())
            except Exception as e:
                logger.error("Error downloading master audio file for conversion: %s" % e)
                logger.debug("Stack trace for download error:\n" + traceback.format_exc())
                raise
            finally:
                #NOTE: This automatically closes the open tmpfd via Python magic, calling os.close(tmpfd) at this point will error.
                destination.close()

        # TODO: check file size against datastream? os.path.getsize(path)

        calculated_checksum = md5sum(wav_file_path)
        if obj.audio.checksum != calculated_checksum:
            raise Exception("Checksum for local audio file %s does not match Fedora datastream checksum %s" % \
                (calculated_checksum, obj.audio.checksum))

        # Call the conversion utility.
        # NOTE: With files greater than 2GB, the visual output from
        # LAME will not be correct, but it will convert and return 0.
        process = subprocess.Popen(['lame', '--preset', 'insane', wav_file_path, mp3_file_path],
                stdout=subprocess.PIPE, preexec_fn=os.setsid, stdin=subprocess.PIPE,
                stderr=subprocess.PIPE)

        # returns a tuple of stdout, stderr. The output of the LAME goes to stderr.
        stdout_output, stderr_output = process.communicate()
        # Return code of the process.
        return_code = process.returncode

        # Ensure success from output, and if so, save the file and remove the temporary files.
        if return_code == 0:
            # Verify the original file and generated mp3 are the same length (within tolerable limits)
            if not check_wav_mp3_duration(wav_file_path=wav_file_path, mp3_file_path=mp3_file_path):
                logger.error("Failed to convert audio file (duration of wav and mp3 did not match) for %s " % pid)
                raise Exception("Error generating MP3 (duration of wav and mp3 did not match)")

            with open(mp3_file_path) as f:
                obj.compressed_audio.content = f
                obj.compressed_audio.checksum = md5sum(mp3_file_path)
                obj.compressed_audio.label = obj.audio.label

                obj.save("Added compressed mp3 audio stream from LAME conversion output.")
            return "Successfully converted file"

        # Raise error if this is reached - if conversion succeded, should have already returned
        logger.error("Failed to convert audio file (LAME failed) for %s" % pid)
        logger.error("LAME output: %s" % stderr_output)
        raise Exception("Failed to convert audio (LAME failed): %s" % stderr_output)

    # General exception catch for logging.
    # possible more specific exceptions:
    # OSError - file open/write error
    # RequestFailed - fedora communication error
    except Exception as e:
        # log the error and then re-raise it
        logger.error("Failed to convert audio for %s : %s" % (pid, e))
        # TODO: may want to return a more detailed error message here
        raise
    #Cleanup for everything.
    finally:
        # remove if file was not passed in or if removal was requested for passed in file
        if (use_wav is None or (use_wav is not None and remove_wav)) \
                            and wav_file_path is not None:
            try:
                if os.path.exists(wav_file_path):
                    os.remove(wav_file_path)
            except OSError as e:
                # log the exception but don't raise it - not a conversion error to report to user
                logger.error("Error removing wav file %s: %s" % (wav_file_path, e))

        # Remove the generated mp3 file, if it exists.
        if mp3_file_path is not None:
            try:
                if os.path.exists(mp3_file_path):
                    os.remove(mp3_file_path)
            except OSError as e:
                # log the exception but don't raise it - not a conversion error to report to user
                logger.error("Error removing mp3 file %s: %s" % (mp3_file_path, e))


def queue_access_copy(obj, **extra_convert_args):
    task = convert_wav_to_mp3.delay(obj.pid, **extra_convert_args)
    # create a task result object to track conversion status
    result = TaskResult(label='Generate MP3', object_id=obj.pid,
        url=obj.get_absolute_url(), task_id=task.task_id)
    result.save()
