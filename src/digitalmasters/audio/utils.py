import hashlib

def md5sum(filename):
    '''Calculate and returns an md5 checksum for the specified file.

    :param filename: name of the file for which checksum should be calculated
    :returns: hex-digest formatted MD5 checksum as a string
    '''
    # pythonic md5 calculation from Stack Overflow 
    # http://stackoverflow.com/questions/1131220/get-md5-hash-of-a-files-without-open-it-in-python
    md5 = hashlib.md5()
    with open(filename,'rb') as f:
        for chunk in iter(lambda: f.read(128*md5.block_size), ''):
             md5.update(chunk)
    return md5.hexdigest()

# TODO: move into common/utils.py