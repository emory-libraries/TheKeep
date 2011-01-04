from celery.decorators import task
from digitalmasters.audio.models import AudioObject
from digitalmasters.fedora import Repository
from django.conf import settings
import subprocess
import logging
import hashlib
import sys
import tempfile
import os

@task
def convertWAVtoMP3(pid):
    try:
        repo = Repository()
        obj = repo.get_object(pid, type=AudioObject)
    
        #Setup the directory for the file download.
        tempdir = settings.INGEST_STAGING_TEMP_DIR
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)

        #returnedMkStemp is a tuple with the name in the 2nd position.
        returnedMkStemp = tempfile.mkstemp(dir=tempdir)
    
        destination = open(returnedMkStemp[1], 'wb+')
        destination.write(obj.audio.content.read())
        destination.close()

        if obj.audio.checksum != md5sum(returnedMkStemp[1]):
            logging.error("Audio file checksum did not match for conversion - pid is: " + obj.pid)
            os.remove(returnedMkStemp[1])
            return "Audio file checksum did not match, file was corrupt, exiting now."

        #Call the conversion utility. 
        process  = subprocess.Popen(['lame', '--preset', 'insane', returnedMkStemp[1], returnedMkStemp[1] + '.mp3'], stdout=subprocess.PIPE, preexec_fn=os.setsid,stdin=subprocess.PIPE,stderr=subprocess.PIPE,)

        #stdout_value will be tuple with stdout in place 0, stderr in place 1. The output of the program will be in place 1.
        stdout_value = process.communicate()


        #Return code of the process.
        return_code = process.returncode
    
        #Ensure success from output, and if so, save the file and remove the temporary files.
        if "(100%)|" in stdout_value[1] and "Writing LAME Tag...done" in stdout_value[1] and return_code == 0:
	    obj.compressed_audio.content = open(returnedMkStemp[1] + ".mp3")
    	    obj.save()
            os.remove(returnedMkStemp[1])
            os.remove(returnedMkStemp[1] + ".mp3")
            return "Successfully converted file"
    
        logging.error("Failed to convert audio file (LAME failed), pid is: " + obj.pid)
        
        #Remove temporary files before returning error.
        os.remove(returnedMkStemp[1])
        os.remove(returnedMkStemp[1] + ".mp3")
        return "Error converting file."
    except Exception as e:
        logging.error("Failed to convert audio file (try...except exception), pid is: " + obj.pid)

def md5sum(fname):
    '''Returns an md5 hash for file fname.'''
    #Try to open the file.
    try:
        f = file(fname, 'rb')
    except:
        return 'Failed to open file'
    
    #Calculate the md5
    m = hashlib.md5()
    while True:
        d = f.read(8096)
        if not d:
            break
        m.update(d)
        
    f.close()
    return m.hexdigest()
