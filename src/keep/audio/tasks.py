import logging
import os
import subprocess
import tempfile
import traceback
from celery.decorators import task

from django.conf import settings

from keep.audio.models import AudioObject, wav_and_mp3_duration_comparator
from keep.common.fedora import Repository
from keep.common.utils import md5sum

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
                logger.error("Error opening temporary file, cannot download master audio for conversion : %s" % e)
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
        
        #Call the conversion utility. 
        #NOTE: With files greater than 2GB, the visual output from LAME will not be correct, but it will convert and return 0.
        process  = subprocess.Popen(['lame', '--preset', 'insane', wav_file_path, mp3_file_path],
                stdout=subprocess.PIPE, preexec_fn=os.setsid, stdin=subprocess.PIPE,
                stderr=subprocess.PIPE)

        #stdout_value will be tuple with stdout in place 0, stderr in place 1. The output of the program will be in place 1.
        stdout_value = process.communicate()

        #Return code of the process.
        return_code = process.returncode
    
        #Ensure success from output, and if so, save the file and remove the temporary files.
        if (return_code == 0):
            #Verify the original file and this file are the same length to within 0.1 seconds.
            if(not wav_and_mp3_duration_comparator(obj_pid=None,wav_file_path=wav_file_path, mp3_file_path=mp3_file_path)):
                logger.error("Failed to convert audio file (duration of wav and mp3 did not match), pid is: " + pid)
                raise Exception("Failed to convert audio file (duration of wav and mp3 did not match), pid is: " + pid)

	    with open(mp3_file_path) as f: 
                obj.compressed_audio.content = f
                obj.compressed_audio.checksum = md5sum(mp3_file_path)
                obj.compressed_audio.label = obj.audio.label
    	        obj.save("Added compressed mp3 audio stream from LAME conversion output.")
            return "Successfully converted file"
    
        # Raise error if this is reached as should have returned "Successfully converted file".
        logger.error("Failed to convert audio file (LAME failed), pid is: " + pid)
        raise Exception("Failed to convert audio file (LAME failed), pid is: " + pid + " output: " + stdout_value[1])
    # General exception catch for logging.
    # possible more specific exceptions:
    # OSError - file open/write error
    # RequestFailed - fedora communication error 
    except Exception as e:
        # log the error and then re-raise it
        logger.error("Failed to convert audio for %s : %s" % (pid, e))
        raise
    #Cleanup for everything.
    finally:
        # remove if file was not passed in or if removal was requested for passed in file
        if (use_wav is None or (use_wav is not None and remove_wav)) \
                            and wav_file_path is not None:
            if os.path.exists(wav_file_path):
                os.remove(wav_file_path)

        # Remove the generated mp3 file, if it exists.
        if mp3_file_path is not None:
            if os.path.exists(mp3_file_path):
                os.remove(mp3_file_path)
         
