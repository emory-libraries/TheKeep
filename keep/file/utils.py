import hashlib
import logging


logger = logging.getLogger(__name__)


def checksum(filename, type):
    '''Calculate and returns a checksum for the specified file.  Any file
    errors (non-existent file, read error, etc.) are not handled here but should
    be caught where this method is called.

    :param filename: full path to the file for which a checksum should be calculated
    :prarm type: any type of hashing algorithm supported by :mod:`hashlib`

    :returns: hex-digest formatted checksum as a string
    '''
    logger.debug('Calculating %s checksum for %s' % (type, filename))
    # pythonic md5 calculation from Stack Overflow
    # http://stackoverflow.com/questions/1131220/get-md5-hash-of-a-files-without-open-it-in-python
    algorithm = getattr(hashlib, type)
    ck = algorithm()
    with open(filename,'rb') as f:
        for chunk in iter(lambda: f.read(128 * ck.block_size), ''):
             ck.update(chunk)
    return ck.hexdigest()


def md5sum(filename):
    '''Calculate and returns an MD5 checksum for the specified file.  Any file
    errors (non-existent file, read error, etc.) are not handled here but should
    be caught where this method is called.

    :param filename: full path to the file for which a checksum should be calculated
    :returns: hex-digest formatted MD5 checksum as a string
    '''
    return checksum(filename, 'md5')

def sha1sum(filename):
    'Calculate and return a SHA-1 hash for a file.  Same usage as :meth:`md5sum`'
    return checksum(filename, 'sha1')



_DUMP_BLOCK_SIZE = 16 * 1024  # mostly arbitrary. this size seems nice.


def dump_post_data(inf, outf, size=None):
    '''Copy data from infile `inf` to outfile `outf` in chunks to avoid
    loading the entirety of a large file into memory. If the
    the `size` is known in advance, read only that many bytes.
    '''
    while True:
        # if we know the size and it's less than a block, then only read
        # that much. if we don't know, or if it's bigger than a block, then
        # read a whole block.
        read_length = _DUMP_BLOCK_SIZE
        if size is not None and size < read_length:
            read_length = size

        # copy a single block of data.
        block = inf.read(read_length)
        if not block:  # EOF from client. that's all she wrote.
            break
        outf.write(block)

        # if we have a content_length, then mark off the bits we copied.
        # if we've read it all, then we're done.
        if size:
            size -= len(block)
        if size == 0:
            break

