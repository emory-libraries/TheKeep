from celery.decorators import task
from digitalmasters.audio.models import AudioObject
from digitalmasters.common.fedora import Repository
from django.conf import settings
from digitalmasters.audio.utils import md5sum
import subprocess
import logging
import sys
import tempfile
import os
import traceback

@task
def convert_wav_to_mp3(pid,overrideErrors=False,existingFilePath=None):
    """Converts a wav file to mp3. Accepted parameters are:
    * pid: the pid of the object to have its audio converted.
    
    * overrideErrors: For non-valid wav files (those over 2GB), LAME will never reported 
                      a completed conversion despite generating what appears to be a
                      valid mp3 file. Hence, this allows one to run the task and accept
                      the generated result regardless of LAME's status for these files.

    * existingFilePath: Rather than getting the WAV content from the fedora object,
                        this will use the file path provided instead. NOTE: Whatever
                        file is used will be deleted after its use.

    In addition, this function currently stores all temporary files in the temporary
    ingest directory (to make cleanup easier and as it is usually part of the ingest
    process.
    """
    
    try:
        repo = Repository()
        obj = repo.get_object(pid, type=AudioObject)
    
        #Setup the directory for the file download. Currently the staging directory.
        tempdir = settings.INGEST_STAGING_TEMP_DIR
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        
        if existingFilePath != None:
            tmpname = existingFilePath
        else:
            #tempfile.mkstemp returns a tuple with a file descriptor in the first position and the full path in the 2nd position.
            tmpfd, tmpname = tempfile.mkstemp(dir=tempdir)
            
            try:
                #destination = os.fdopen(tmpfd, 'wb+')
                destination = open(tmpname, 'wb+')
            except:
                msg = traceback.format_exc() 
                logging.error("Failed to convert audio file (file could not be open from file descriptor), pid is: " + pid + " and exception is: " + msg)
                os.close(tmpfd)
                raise
            
            try:
                destination.write(obj.audio.content.read())
            except:
                msg = traceback.format_exc() 
                logging.error("Failed to convert audio file (file could not be open or written), pid is: " + pid + " and exception is: " + msg)
                raise
            finally:
                destination.close()

        if obj.audio.checksum != md5sum(tmpname):
            logging.error("Audio file checksum did not match for conversion - pid is: " + pid)
            os.remove(tmpname)
            raise Exception("celery","Audio file checksum did not match for conversion - pid is: " + pid)

        #Call the conversion utility. 
        process  = subprocess.Popen(['lame', '--preset', 'insane', tmpname, tmpname + '.mp3'], stdout=subprocess.PIPE, preexec_fn=os.setsid, stdin=subprocess.PIPE, stderr=subprocess.PIPE,)

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
            os.remove(tmpname)
            os.remove(tmpname+".mp3")
            return "Successfully converted file"
    
        logging.error("Failed to convert audio file (LAME failed), pid is: " + pid)
        #Remove temporary files before returning error.
        os.remove(tmpname)
        os.remove(tmpname+".mp3")
        raise Exception("celery","Failed to convert audio file (LAME failed), pid is: " + pid)
    #General exception catch for logging.
    except:
        msg = traceback.format_exc() 
        logging.error("Failed to convert audio file (try...except exception), pid is: " + pid + " and exception is: " + msg)
        #If a file was passed in, still remove it:
        if existingFilePath != None:
            os.remove(existingFilePath)
        #Still raise the error.
        raise

