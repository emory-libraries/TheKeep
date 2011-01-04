import os
import hashlib
import sys

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
