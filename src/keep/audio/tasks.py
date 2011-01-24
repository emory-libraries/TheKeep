import logging
import os
import subprocess
import tempfile
import traceback
from celery.decorators import task

from django.conf import settings

from keep.audio.models import AudioObject
from keep.common.fedora import Repository
from keep.common.utils import md5sum

logger = logging.getLogger(__name__)

@task
def convert_wav_to_mp3(pid,overrideErrors=False,existingFilePath=None):
    """Converts a wav file to mp3. Accepted parameters are:
    * pid: the pid of the object to have its audio converted.
    
    * overrideErrors: For non-valid wav files (those over 2GB), LAME will never reported 
                      a completed conversion despite generating what appears to be a
                      valid mp3 file. Hence, this allows one to run the task and accept
                      the generated result regardless of LAME's status for these files.

    * existingFilePath: Rather than getting the WAV content from the fedora object,
                        this will use the file path provided instead.  The file
                        provided **must** match the checksum for the master audio
                        datastream in the fedora object, or conversion will fail.

    In addition, this function currently stores all temporary files in the temporary
    ingest directory (to make cleanup easier and as it is usually part of the ingest
    process.
    """
    try:
        repo = Repository()
        obj = repo.get_object(pid, type=AudioObject)
    
        # set up temp directory where file to be converted will be downloaded
        # (if necessary) and where the generated mp3 will be created
        tempdir = settings.INGEST_STAGING_TEMP_DIR
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        
        if existingFilePath != None:
            tmpname = existingFilePath
        else:
            # download the master audio file from the object in fedora
            # mkstemp returns file descriptor and full path to the temp file
            tmpfd, tmpname = tempfile.mkstemp(dir=tempdir)       
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

            # check file size against datastream? os.path.getsize(path)

        calculated_checksum = md5sum(tmpname)
        if obj.audio.checksum != calculated_checksum:
            raise Exception("Checksum for local audio file %s does not match Fedora datastream checksum %s" % \
                (calculated_checksum, obj.audio.checksum))            

        #Call the conversion utility. 
        process  = subprocess.Popen(['lame', '--preset', 'insane', tmpname, tmpname + '.mp3'],
                stdout=subprocess.PIPE, preexec_fn=os.setsid, stdin=subprocess.PIPE,
                stderr=subprocess.PIPE)

        #stdout_value will be tuple with stdout in place 0, stderr in place 1. The output of the program will be in place 1.
        stdout_value = process.communicate()

        #Return code of the process.
        return_code = process.returncode
    
        #Ensure success from output, and if so, save the file and remove the temporary files.
        if ((overrideErrors == True) or ("(100%)|" in stdout_value[1] and "Writing LAME Tag...done" in stdout_value[1]) and return_code == 0):
	    with open(tmpname+".mp3") as f: 
                obj.compressed_audio.content = f
                obj.compressed_audio.checksum = md5sum(tmpname + ".mp3")
                obj.compressed_audio.label = obj.audio.label
    	        obj.save("Added compressed mp3 audio stream from LAME conversion output.")
            return "Successfully converted file"
    
        #Raise error if this is reached as should have returned "Successfully converted file".
        logger.error("Failed to convert audio file (LAME failed), pid is: " + pid)
        raise Exception("celery","Failed to convert audio file (LAME failed), pid is: " + pid)
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
        # Only remove if file was not passed in (ie. only remove the temporary file).
        if existingFilePath is None and tmpname is not None:
            if os.path.exists(tmpname):
                os.remove(tmpname)

        #Remove the generated mp3 file, if it exists.
        if os.path.exists(tmpname+".mp3"):
            os.remove(tmpname+".mp3")
         
