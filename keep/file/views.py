import logging
import magic
import os
import tempfile
import time
import traceback

from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseForbidden, \
    HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from eulcommon.djangoextras.http import HttpResponseSeeOtherRedirect, \
    HttpResponseUnsupportedMediaType
from eulcommon.djangoextras.auth.decorators import permission_required_with_ajax


from keep.common.utils import md5sum  # TODO: move into file.utils

logger = logging.getLogger(__name__)


# TODO: generate list from supported upload objects
allowed_upload_types = ['audio/x-wav', 'audio/wav']


@permission_required_with_ajax('common.marbl_allowed')
@csrf_exempt  # TODO: should pass CSRF token instead
def ajax_upload(request):
    """Process a file uploaded via AJAX and store it in a temporary staging
    directory for subsequent ingest into the repository.  The request must
    include the following headers:

         * Content-Disposition, e.g. filename="original_name.wav"
         * Content-MD5: MD5 checksum of the file calculated before upload

    If the file is successfully uploaded and passes checks on file type
    (must be in a configured list of allowed types) and MD5 checksum (the
    checksum calculated for the uploaded file must match the checksum passed in
    the request), then the file will be stored in the ingest staging directory
    and a staging file identifier will be returned in the body of the response.

    To avoid calculating MD5 checksums multiple times, the MD5 for the file
    will also be stored in the ingest staging directory, in a file named the same
    as the staging temporary filename with '.md5' added.

    Note that while the Content-Disposition header is technically intended for use
    in HTTP responses, we're using it here in HTTP requests because it is a
    good fit for our purpose.
    """
    # NOTE: size and type request headers unused?

    # Setup the directory for the file upload.
    staging_dir = settings.INGEST_STAGING_TEMP_DIR
    # FIXME: this should happen only *once* somewhere... where?
    if not os.path.exists(staging_dir):
        os.makedirs(staging_dir)

    try:
        content_disposition = request.META['HTTP_CONTENT_DISPOSITION']
    except KeyError:
        return HttpResponseBadRequest('Content-Disposition header is required',
                                      content_type='text/plain')
    if 'filename=' not in content_disposition:
        return HttpResponseBadRequest('Content-Disposition header must include filename',
                                      content_type='text/plain')
    try:
        client_md5 = request.META['HTTP_CONTENT_MD5']
    except KeyError:
        return HttpResponseBadRequest('Content-MD5 header is required',
                                      content_type='text/plain')

    # content disposition could be something like 'attachment; filename="foo"
    if ';' in content_disposition:
        dispo = content_disposition.split(';')
        for d in dispo:
            if d.strip().startswith('filename='):
                filename = d.strip()[len('filename='):].strip('"')
    else:
        filename = content_disposition[len('filename='):].strip('"')

    file_base, file_extension = os.path.splitext(filename)

    # create a temporary file based on the name of the original file
    with tempfile.NamedTemporaryFile(mode='wb+', suffix=file_extension,
                                     prefix='%s_' % file_base, dir=staging_dir,
                                     delete=False) as upload:
        try:
            content_length = long(request.environ['CONTENT_LENGTH'])
        except:
            content_length = None

        # request.raw_post_data would force us to read the entire file
        # contents into memory before writing it, which could be problematic
        # if the file is large. reading instead straight from wsgi.input
        # allows us to handle it a chunk at a time
        _dump_post_data(request.environ['wsgi.input'], upload, content_length)
        upload_file = upload.name

    ingest_file = os.path.basename(upload_file)
    logger.debug('wrote ' + ingest_file)

    try:
        # ignoring request mimetype since it is unreliable
        m = magic.Magic(mime=True)
        type = m.from_file(upload_file)
        type, separator, options = type.partition(';')
        if type not in allowed_upload_types:
            os.remove(upload_file)
            # send response with status 415 Unsupported Media Type
            return HttpResponseUnsupportedMediaType('File type %s is not allowed' % type,
                                                    content_type='text/plain')
    except Exception as e:
        logger.debug(e)

    # Calculate an MD5 for the uploaded file and compare with the client-calculated
    # MD5 to make sure that the entire file was uploaded correctly
    try:
        start = time.time()
        calculated_md5 = md5sum(upload_file)
        logger.debug('Calculated MD5 checksum for %s: %s (took %f secs)' %
                    (filename, calculated_md5, time.time() - start))
        if calculated_md5 != client_md5:
            logger.debug('calculated md5 %s did not match request MD5 %s' %
                        (calculated_md5, client_md5))
            return HttpResponseBadRequest('Checksum mismatch; uploaded data may be incomplete or corrupted',
                                          content_type='text/plain')

        # if the MD5 check passes, store the MD5 so we don't have to calculate it again
        with open(os.path.join(staging_dir, ingest_file + '.md5'), 'w') as md5file:
            md5file.write(calculated_md5)

    except Exception as e:
        logger.error(e)
        logger.debug("Error details:\n" + traceback.format_exc())

    # success: return the name of the staging file to be used for ingest
    return HttpResponse(ingest_file, content_type='text/plain')


# TODO: move into file.util (?)

_DUMP_BLOCK_SIZE = 16 * 1024  # mostly arbitrary. this size seems nice.


def _dump_post_data(inf, outf, size=None):
    '''Copy data from `inf` to `outf` in chunks. If the caller happens to
    know the `size` in advance, read only that many bytes.
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

