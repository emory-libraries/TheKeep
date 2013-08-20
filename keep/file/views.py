import json
import logging
import magic
import os
import tempfile
import time
import traceback

from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.utils.safestring import mark_safe


from eulcommon.djangoextras.http import HttpResponseUnsupportedMediaType
from eulcommon.djangoextras.auth.decorators import permission_required_with_ajax
from eulfedora.util import RequestFailed
from eulfedora.views import raw_datastream, raw_audit_trail


from keep.audio.models import AudioObject
from keep.audio.tasks import queue_access_copy
from keep.collection.models import CollectionObject
from keep.common.fedora import Repository, TypeInferringRepository, history_view
from keep.file.forms import UploadForm
from keep.file.models import DiskImage
from keep.file.utils import md5sum, dump_post_data


logger = logging.getLogger(__name__)


uploadable_objects = [AudioObject, DiskImage]
# TODO: document requirements for repo objects to be included here
# - list of allowed mimetypes
# - static class method to init from file


# generate list of allowed upload mimetypes based on objects we support
allowed_upload_types = []
for a in uploadable_objects:
    allowed_upload_types.extend(a.allowed_mimetypes)



@permission_required_with_ajax('common.marbl_allowed')
def upload(request):
    '''Upload file(s) and create new fedora :class:`~keep.audio.models.AudioObject` (s).
    Only accepts audio/x-wav currently.

    There are two distinct ways to upload file. The first case is
    kicked off when "fileManualUpload" exists in the posted form. If
    it does, then this was not a HTML5 browser, and the file upload
    occurs as is usual for a single file upload.

    In the other approach, the file was uploaded via a HTML5 ajax
    upload already. In this case, we are reading in various hidden
    generated form fields that indicate what was uploaded from the
    javascript code.
    '''
    repo = Repository()


    ctx_dict = {
        # list of allowed file types, in a format suited for passing to javascript
        'js_allowed_types': mark_safe(json.dumps(allowed_upload_types))
    }

    if request.method == 'POST':
        content_type = request.META.get('CONTENT_TYPE', 'application/octet-stream')
        media_type, sep, options = content_type.partition(';')
        # content type is technically case-insensitive; lower-case before comparing
        media_type = media_type.strip().lower()

        # if form has been posted, process & ingest files
        if media_type == 'multipart/form-data':

            # check for a single file upload
            form = UploadForm(request.POST, request.FILES)

            # If form is not valid (i.e., no collection specified, no
            # or mismatched files uploaded), bail out and redisplay
            # form with any error messages.
            if not form.is_valid():
                ctx_dict['form'] = form
                return render(request, 'file/upload.html', ctx_dict)

            # Form is valid. Get collection & check for optional comment
            collection = repo.get_object(pid=form.cleaned_data['collection'],
                                         type=CollectionObject)
            # get user comment if any; default to a generic ingest comment
            comment = form.cleaned_data['comment'] or 'initial repository ingest'
            # get dictionary of file path -> filename, based on form data
            files_to_ingest = form.files_to_ingest()


            # process all files submitted for ingest (single or batch mode)
            if files_to_ingest:
                results = ingest_files(files_to_ingest, collection, comment, request)

                # add per-file ingest result status to template context
                ctx_dict['ingest_results'] = results
                # after processing files, fall through to display upload template

        else:
            # POST but not form data - handle ajax file upload
            return ajax_upload(request)

    # on GET or non-ajax POST, display the upload form
    ctx_dict['form'] = UploadForm()
    # convert list of allowed types for passing to javascript

    return render(request, 'file/upload.html', ctx_dict)
    # NOTE: previously, this view set the response status code to the
    # Fedora error status code if there was one.  Since this view now processes
    # multiple files for ingest, simply returning 200 if processing ends normally.


def ingest_files(files, collection, comment, request):
    '''Ingest a dictionary of files as returned by
    :meth:`keep.files.forms.UploadForm.files_to_ingest`.
    Returns a dictionary reporting per-file ingest success or failure.

    :param files: dictionary of files to be ingested
    :param collection: :class:`~keep.collection.models.CollectionObject` that
        newly ingested objects should be associated with
    :param comment: save message for fedora ingest
    :param request: :class:`~django.http.HttpRequest`, to access Fedora and
        ingest new objects as the logged-in user.
    '''

    # NOTE: using this structure for easy of display in django templates (e.g., regroup)
    results = []

    m = magic.Magic(mime=True)
    for filename, label in files.iteritems():

        file_info = {'label': label}

        # check if file is an allowed type

        # NOTE: for single-file upload, browser-set type is
        # available as UploadedFile.content_type - but since
        # browser mimetypes are unreliable, calculate anyway
        try:
            type = m.from_file(filename)
        except IOError:
            raise Exception('Uploaded file is no longer available for ingest; please try again.')

        type, separator, options = type.partition(';')
        if type not in allowed_upload_types:
            # store error for display on detailed result page
            file_info.update({'success': False,
                              'message': '''File type '%s' is not allowed''' % type})
            # if not an allowed type, no further processing
            continue

        if collection is None:
            file_info.update({'success': False,
                              'message': '''Collection not selected'''})
            continue

        # if there is an MD5 file (i.e., file was uploaded via ajax),
        # use the contents of that file as checksum
        if os.path.exists(filename + '.md5'):
            with open(filename + '.md5') as md5file:
                md5 = md5file.read()
        # otherwise, calculate the MD5 (single-file upload)
        else:
            md5 = md5sum(filename)

        # determine what type of object to initialize based on mimetype
        objtype = None
        for t in uploadable_objects:
            if type in t.allowed_mimetypes:
                objtype = t
                break

        # initialize a new object from the file
        obj = objtype.init_from_file(filename, initial_label=label,
                                     request=request, checksum=md5)

        # set collection on ingest
        obj.collection = collection

        try:
            # NOTE: by sending a log message, we force Fedora to store an
            # audit trail entry for object creation, which doesn't happen otherwise
            obj.save(comment)
            file_info.update({'success': True, 'pid': obj.pid,
                              'url': obj.get_absolute_url()})

            # Start asynchronous task to convert audio for access
            queue_access_copy(obj, use_wav=filename, remove_wav=True)

            # NOTE: could remove MD5 file (if any) here, but MD5 files
            # should be small and will get cleaned up by the cron script

        except Exception as e:
            logger.error('Error ingesting %s: %s' % (filename, e))
            logger.debug("Error details:\n" + traceback.format_exc())
            file_info['success'] = False

            # check for Fedora-specific errors
            if isinstance(e, RequestFailed):
                if 'Checksum Mismatch' in e.detail:
                    file_info['message'] = 'Ingest failed due to a checksum mismatch - ' + \
                        'file may have been corrupted or incompletely uploaded to Fedora'
                else:
                    file_info['message'] = 'Fedora error: ' + unicode(e)

            # non-fedora error
            else:
                file_info['message'] = 'Ingest failed: ' + unicode(e)

        finally:
            # no matter what happened, store results for reporting to user
            results.append(file_info)

    return results



@permission_required_with_ajax('common.marbl_allowed')
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
        dump_post_data(request.environ['wsgi.input'], upload, content_length)
        upload_file = upload.name

    ingest_file = os.path.basename(upload_file)
    logger.debug('wrote ' + ingest_file)

    try:
        # ignoring request mimetype since it is unreliable
        m = magic.Magic(mime=True)
        type = m.from_file(upload_file)
        logger.debug('mimetype for %s detected as %s' % (ingest_file, type))
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


@permission_required("common.marbl_allowed")
def view(request, pid):
    '''View a single repository item.

    Currently has bare minimum implementation to support ingesting
    :class:`~keep.file.models.DiskImage` content (new object url is required).
    '''
    # repo = TypeInferringRepository(request=request)
    repo = Repository(request=request)
    obj = repo.get_object(pid)
    if not obj.exists:
        raise Http404

    # this view isn't implemented yet, but we want to be able to use the
    # uri. so if someone requests the uri, send them straight to the edit
    # page for now.
    return render(request, 'file/view.html', {'obj': obj})


### FIXME: these views are currently redundant; consolidate all and make the
# file versions the common ones?

@permission_required("common.arrangement_allowed")
def view_datastream(request, pid, dsid):
    'Access raw object datastreams'
    # initialize local repo with logged-in user credentials & call generic view
    # use type-inferring repo to pick up rushdie file or generic arrangement
    response = raw_datastream(request, pid, dsid,
                          repo=TypeInferringRepository(request=request))

    # work-around for email MIME data : display as plain text so it
    # can be viewed in the browser
    if response['Content-Type'] == 'message/rfc822':
        response['Content-Type'] = 'text/plain'
    return response


@permission_required("common.arrangement_allowed")
def view_audit_trail(request, pid):
    'Access XML audit trail'
    # initialize local repo with logged-in user credentials & call eulfedora view
    # type shouldn't matter for audit trail
    return raw_audit_trail(request, pid, repo=Repository(request=request))


@permission_required("common.arrangement_allowed")
def history(request, pid):
    'Display human-readable audit trail information.'
    return history_view(request, pid, template_name='arrangement/history.html')


