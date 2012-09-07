from datetime import date, timedelta
import json
import logging
import magic
import os
import tempfile
import time
import traceback

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseForbidden, \
    HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.template import RequestContext
from django.utils import simplejson
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt

from eulcm.xmlmap.boda import Rights
from eulcommon.djangoextras.auth.decorators import permission_required_with_ajax
from eulcommon.djangoextras.http import HttpResponseSeeOtherRedirect, HttpResponseUnsupportedMediaType
from eulfedora.views import raw_datastream, raw_audit_trail
from eulfedora.util import RequestFailed, PermissionDenied
from eulfedora.models import DigitalObjectSaveFailure

from keep.audio import forms as audioforms
from keep.audio.models import AudioObject
from keep.audio.feeds import feed_items
from keep.audio.tasks import queue_access_copy
from keep.collection.models import CollectionObject 
from keep.common.fedora import Repository, history_view
from keep.common.utils import md5sum

logger = logging.getLogger(__name__)

allowed_audio_types = ['audio/x-wav', 'audio/wav']

@permission_required_with_ajax('common.marbl_allowed')
@csrf_exempt
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
        'js_allowed_types': mark_safe(json.dumps(allowed_audio_types))
    }

    if request.method == 'POST':
        content_type = request.META.get('CONTENT_TYPE', 'application/octet-stream')        
        media_type, sep, options = content_type.partition(';')
        # content type is technically case-insensitive; lower-case before comparing
        media_type = media_type.strip().lower()

        # if form has been posted, process & ingest files
        if media_type  == 'multipart/form-data':

            # check for a single file upload
            form = audioforms.UploadForm(request.POST, request.FILES)
            
            # If form is not valid (i.e., no collection specified, no
            # or mismatched files uploaded), bail out and redisplay
            # form with any error messages.
            if not form.is_valid():
                ctx_dict['form'] = form
                return render(request, 'audio/upload.html', ctx_dict)

            # Form is valid. Get collection & check for optional comment
            collection = repo.get_object(pid=form.cleaned_data['collection'],
                                         type=CollectionObject)
            # get user comment if any; default to a generic ingest comment
            comment = form.cleaned_data['comment'] or 'ingesting audio'
            # get dictionary of file path -> filename, based on form data
            files_to_ingest = form.files_to_ingest()
            

            results = []
            # results will be a list of dictionary to report per-file ingest success/failure
            # NOTE: using this structure for easy of display in django templates (e.g., regroup)
            
            # process all files submitted for ingest (single or batch mode)
            if files_to_ingest:
                # TODO: break this out into a separate function
                m = magic.Magic(mime=True)
                for filename, label in files_to_ingest.iteritems():
                    try:
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
                        if type not in allowed_audio_types:
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
                        # initialize a new audio object from the file
                        obj = AudioObject.init_from_file(filename,
                                    initial_label=label, request=request,                                    
                                    checksum=md5)

                        #set collection on ingest
                        obj.collection = collection

                        # NOTE: by sending a log message, we force Fedora to store an
                        # audit trail entry for object creation, which doesn't happen otherwise
                        obj.save(comment)
                        file_info.update({'success': True, 'pid': obj.pid})
                        # Start asynchronous task to convert audio for access
                        queue_access_copy(obj, use_wav=filename,
                                          remove_wav=True)

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

            # add per-file ingest result status to template context
            ctx_dict['ingest_results'] = results
            # after processing files, fall through to display upload template

        else:
            # POST but not form data - handle ajax file upload
            return ajax_file_upload(request)
            
    # on GET or non-ajax POST, display the upload form
    ctx_dict['form'] = audioforms.UploadForm()
    # convert list of allowed types for passing to javascript

    return render(request, 'audio/upload.html', ctx_dict)
    # NOTE: previously, this view set the response status code to the
    # Fedora error status code if there was one.  Since this view now processes
    # multiple files for ingest, simply returning 200 if processing ends normally.

@permission_required_with_ajax('common.marbl_allowed')
@csrf_exempt
def ajax_file_upload(request):
    """Process a file uploaded via AJAX and store it in a temporary staging 
    directory for subsequent ingest into the repository.  The request must
    include the following headers:

         * Content-Disposition: filename="original_name.wav"          
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

    #Setup the directory for the file upload.
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

    # content disposition could be something like 'attachment; filename="foo"
    if ';' in content_disposition:
        dispo = content_disposition.split(';')
        for d in dispo:
            if d.strip().startswith('filename='):
                filename = d.strip()[len('filename='):].strip('"')
    else:
        filename = content_disposition[len('filename='):].strip('"')

    try:
        client_md5 = request.META['HTTP_CONTENT_MD5']
    except KeyError:
        return HttpResponseBadRequest('Content-MD5 header is required',
                    content_type='text/plain')

    file_base, file_extension = os.path.splitext(filename)

    # create a temporary file based on the name of the original file
    with tempfile.NamedTemporaryFile(mode='wb+', suffix=file_extension,
                   prefix='%s_' % file_base, dir=staging_dir, delete=False) as upload:
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
        if type not in allowed_audio_types:
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
            logger.debug('calculated md5 %s did not match request MD5 %s' % \
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

_DUMP_BLOCK_SIZE = 16 * 1024 # mostly arbitrary. this size seems nice.
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
        if not block: # EOF from client. that's all she wrote.
            break
        outf.write(block)

        # if we have a content_length, then mark off the bits we copied.
        # if we've read it all, then we're done.
        if size:
            size -= len(block)
        if size == 0:
            break

@permission_required("common.marbl_allowed")
def view(request, pid):
    '''View a single :class:`~keep.audio.models.AudioObject`.
    Not yet implemented; for now, redirects to :meth:`edit` view.
    '''
    # this view isn't implemented yet, but we want to be able to use the
    # uri. so if someone requests the uri, send them straight to the edit
    # page for now.
    return HttpResponseSeeOtherRedirect(reverse('audio:edit',
                kwargs={'pid': pid}))

@permission_required("common.marbl_allowed")
def view_datastream(request, pid, dsid):
    'Access raw object datastreams (MODS, RELS-EXT, DC, DigitalTech, SourceTech, JHOVE)'
    # initialize local repo with logged-in user credentials & call generic view
    return raw_datastream(request, pid, dsid, type=AudioObject,
                          repo=Repository(request=request))

@permission_required("common.marbl_allowed")
def view_audit_trail(request, pid):
    'Access XML audit trail for an audio object'
    # initialize local repo with logged-in user credentials & call eulfedora view
    # FIXME: redundant across collection/arrangement/audio apps; consolidate?
    return raw_audit_trail(request, pid, type=AudioObject,
                           repo=Repository(request=request))


@permission_required("common.marbl_allowed")
def edit(request, pid):
    '''Edit the metadata for a single :class:`~keep.audio.models.AudioObject`.'''
    repo = Repository(request=request)
    obj = repo.get_object(pid, type=AudioObject)
    try:
        # if this is not actually an AudioObject, then 404 (object is not available at this url)
        if not obj.has_requisite_content_models:
            raise Http404
        
        if request.method == 'POST':
            # if data has been submitted, initialize form with request data and object mods
            form = audioforms.AudioObjectEditForm(request.POST, instance=obj)
            if form.is_valid():     # includes schema validation
                # update foxml object with data from the form
                form.update_instance()      # instance is reference to mods object
                if form.comments.cleaned_data.has_key('comment') and form.comments.cleaned_data['comment']:
                    comment = form.comments.cleaned_data['comment']
                else:
                    comment = "update metadata"
                    
                obj.save(comment)
                messages.success(request, 'Successfully updated <a href="%s">%s</a>' % \
                        (reverse('audio:edit', args=[pid]), pid))
                # save & continue functionality - same as collection edit
                if '_save_continue' not in request.POST:
                    return HttpResponseSeeOtherRedirect(reverse('site-index'))
                # otherwise - fall through to display edit form again

            # form was posted but not valid
            else:
                # if we attempted to save and failed, add a message since the error
                # may not be obvious or visible in the first screenful of the form
                messages.error(request,
                    '''Your changes were not saved due to a validation error.
                    Please correct any required or invalid fields indicated below and save again.''')

        else:
            # GET - display the form for editing, pre-populated with content from the object
            form = audioforms.AudioObjectEditForm(instance=obj)

        return render(request, 'audio/edit.html', {'obj' : obj, 'form': form })

    except PermissionDenied:
        # Fedora may return a PermissionDenied error when accessing a datastream
        # where the datastream does not exist, object does not exist, or user
        # does not have permission to access the datastream

        # check that the object exists - if not, 404        
        if not obj.exists:
            raise Http404
        # for now, assuming that if object exists and has correct content models,
        # it will have all the datastreams required for this view

        return HttpResponseForbidden('Permission Denied to access %s' % pid,
                                     mimetype='text/plain')

    except RequestFailed as rf:
        # if fedora actually returned a 404, propagate it
        if rf.code == 404:
            raise Http404
        
        msg = 'There was an error contacting the digital repository. ' + \
              'This prevented us from accessing audio data. If this ' + \
              'problem persists, please alert the repository ' + \
              'administrator.'
        return HttpResponse(msg, mimetype='text/plain', status=500)
        


@permission_required("common.marbl_allowed")
def history(request, pid):
    return history_view(request, pid, type=AudioObject,
                        template_name='audio/history.html')


# download audio must be accessed by iTunes kiosk - should be IP restricted at apache level
# cannot be restricted to staff only here
def download_audio(request, pid, type, extension=None):
    '''Serve out an audio datastream for the fedora object specified by pid.
    Can be used to download original (WAV) audio file or the access copy (MP3).
    
    :param pid: pid of the :class:`~keep.audio.models.AudioObject` instance
        from which the audio datastream should be returned
    :param type: which audio datastream to return - should be one of 'original'
        or 'access'
    :param extension: optional filename extension for access copy to
        distinguish between different types of access copies (currently MP3 or M4A)

    The :class:`django.http.HttpResponse` returned will have a Content-Disposition
    set to prompt the user to download the file with a filename based on the
    object noid and an appropriate file extension for the type of audio requested.
    '''
    repo = Repository(request=request)
    # retrieve the object so we can use it to set the download filename
    obj = repo.get_object(pid, type=AudioObject)
    # determine which datastream is requsted & set datastream id & file extension
    if type == 'original':
        dsid = AudioObject.audio.id
        file_ext = 'wav'
    elif type == 'access':
        dsid = AudioObject.compressed_audio.id
        # make sure the requested file extension matches the datastream
        if (obj.compressed_audio.mimetype == 'audio/mp4' and \
           extension != 'm4a') or \
           (obj.compressed_audio.mimetype == 'audio/mpeg' and \
           extension != 'mp3'):
            raise Http404
        file_ext = extension
    else:
        # any other type is not supported
        raise Http404
    extra_headers = {
        'Content-Disposition': "attachment; filename=%s.%s" % (obj.noid, file_ext)
    }
    # use generic raw datastream view from eulfedora
    return raw_datastream(request, pid, dsid, type=AudioObject,
            repo=repo, headers=extra_headers)
    # errors accessing Fedora will fall through to default 500 error handling

@permission_required("common.marbl_allowed")
def feed_list(request):
    '''List and link to all current iTunes podcast feeds based on the
    number of objects currently available for inclusion in the feeds.'''
    paginated_objects = Paginator(feed_items(),
                                  settings.MAX_ITEMS_PER_PODCAST_FEED)
    return render(request, 'audio/feed_list.html', {
        'per_page': settings.MAX_ITEMS_PER_PODCAST_FEED,
        'pages': paginated_objects.page_range,
        })

@permission_required("common.marbl_allowed")
def queue_generate_access_copy(request, pid):
    '''
    Generates access copy for audio item for pid from AJAX request.
    Returns 'queued' on success and 'error' on any error.

    :param pid: The pid of the object to be generated.
        from.
    '''
    ret = "queued"

    # TODO May want to prevent queuing of more than one at a time or within a time period.
    # TODO For now javascript disables the link until the page is refreshed.
    try:
        repo = Repository(request=request)
        obj = repo.get_object(pid, type=AudioObject)
        queue_access_copy(obj)
    except:
        ret = "error"

    return HttpResponse(simplejson.dumps({'return':ret}), content_type='application/json')