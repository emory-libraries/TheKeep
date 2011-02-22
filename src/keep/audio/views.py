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
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseForbidden, \
    HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt



from eulcore.django.http import HttpResponseSeeOtherRedirect, HttpResponseUnsupportedMediaType
from eulcore.django.taskresult.models import TaskResult
from eulcore.fedora.util import RequestFailed, PermissionDenied
from eulcore.fedora.models import DigitalObjectSaveFailure

from keep.audio import forms as audioforms
from keep.audio.models import AudioObject
from keep.audio.tasks import convert_wav_to_mp3
from keep.collection.models import get_cached_collection_dict
from keep.common.fedora import Repository
from keep.common.utils import md5sum

logger = logging.getLogger(__name__)

allowed_audio_types = ['audio/x-wav', 'audio/wav']

@permission_required('is_staff')  # sets ?next=/audio/ but does not return back here
def index(request):
    search = audioforms.ItemSearch()
    return render_to_response('audio/index.html', {'search' : search},
            context_instance=RequestContext(request))

@permission_required('is_staff')
@csrf_exempt
def upload(request):
    '''Upload file(s) and create new fedora :class:`~keep.audio.models.AudioObject` (s).
    Only accepts audio/x-wav currently.
    
    There are two distinct ways to upload file. The first case is kicked off when "fileManualUpload"
    exists in the posted form. If it does, then this was not a HTML5 browser, and the file upload
    occurs as is usual for a single file upload.

    In the other approach, the file was uploaded via a HTML5 ajax upload already. In this case, we
    are reading in various hidden generated form fields that indicate what was uploaded from the 
    javascript code.
    '''

    ctx_dict = {}

    if request.method == 'POST':
        content_type = request.META.get('CONTENT_TYPE', 'application/octet-stream')        
        media_type, sep, options = content_type.partition(';')
        # content type is technically case-insensitive; lower-case before comparing
        media_type = media_type.strip().lower()

        # if form has been posted, process & ingest files
        if media_type  == 'multipart/form-data':

            # place-holder for files to be ingested, either from single-file upload
            # or batch upload; should be added to the dictionary as filepath: initial label
            files_to_ingest = {}

            # check for a single file upload
            form = audioforms.UploadForm(request.POST, request.FILES)
            # file is the only required field here, so if valid, process single file
            if form.is_valid():
                uploaded_file = request.FILES['audio']
                # initial label now optional on single-file upload form
                initial_label = form.cleaned_data['label']
                # if not specified, use filename
                if not initial_label:
                    initial_label = uploaded_file.name

                files_to_ingest[uploaded_file.temporary_file_path()] = initial_label

            # check for any batch-upload files
            if request.POST.has_key('fileUploads'):                
                uploaded_files = request.POST.getlist('fileUploads')
                filenames = request.POST.getlist('originalFileNames')

                if len(uploaded_files) != len(filenames):
                    # this shouldn't happen unless the javascript uploader does something weird
                    messages.error(request,
                        'Could not correlate uploaded files with original filenames (invalid form data)')
                else:
                    for index in range(len(uploaded_files)):
                        # calculate full path to upload file and add to files to be processed
                        filepath = os.path.join(settings.INGEST_STAGING_TEMP_DIR,
                                                    uploaded_files[index])
                        files_to_ingest[filepath] = filenames[index]

            results = []
            # results will be a list of dictionary to report per-file ingest success/failure
            # NOTE: using this structure for easy of display in django templates (e.g., regroup)
            
            # process all files submitted for ingest (single or batch mode)
            if files_to_ingest:            
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
                        obj.save()
                        file_info.update({'success': True, 'pid': obj.pid})
                        # Start asynchronous task to convert audio for access
                        result = convert_wav_to_mp3.delay(obj.pid, use_wav=filename,
                            remove_wav=True)    # remove after, since ingest is done
                        # create a task result object to track conversion status
                        task = TaskResult(label='Generate MP3', object_id=obj.pid,
                            url=obj.get_absolute_url(), task_id=result.task_id)
                        task.save()

                        # NOTE: could remove MD5 file (if any) here, but MD5 files
                        # should be small and will get cleaned up by the cron script

                    except Exception as e:
                        logging.error('Error ingesting %s: %s' % (filename, e))
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
    ctx_dict['js_allowed_types'] = mark_safe(json.dumps(allowed_audio_types))

    return render_to_response('audio/upload.html', ctx_dict,
                                  context_instance=RequestContext(request))
    # NOTE: previously, this view set the response status code to the
    # Fedora error status code if there was one.  Since this view now processes
    # multiple files for ingest, simply returning 200 if processing ends normally.

@permission_required('is_staff')
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

    
@permission_required('is_staff')
def search(request):
    '''Search for  :class:`~keep.audio.models.AudioObject` by pid,
    title, description, collection, date, or rights.'''
    response_code = None
    form = audioforms.ItemSearch(request.GET, prefix='audio')
    ctx_dict = {'search': form}
    if form.is_valid():
        search_opts = {
            'type': AudioObject,
            # restrict to objects in configured pidspace
            'pid__contains': '%s*' % settings.FEDORA_PIDSPACE,
            # restrict by cmodel in dc:format
            'format__contains': AudioObject.AUDIO_CONTENT_MODEL,
        }
        if form.cleaned_data['pid']:
            search_opts['pid__contains'] = '%s' % form.cleaned_data['pid']
            # add a wildcard if the search pid is the initial value
            if form.cleaned_data['pid'] == form.fields['pid'].initial:
                search_opts['pid__contains'] += '*'
        if form.cleaned_data['title']:
            search_opts['title__contains'] = form.cleaned_data['title']
        if form.cleaned_data['description']:
            search_opts['description__contains'] = form.cleaned_data['description']
        if form.cleaned_data['collection']:
            search_opts['relation__contains'] = form.cleaned_data['collection']
        if form.cleaned_data['date']:
            search_opts['date__contains'] = form.cleaned_data['date']
        if form.cleaned_data['rights']:
            search_opts['rights__contains'] = form.cleaned_data['rights']

        # collect non-empty, non-default search terms to display to user on results page
        search_info = {}
        for field, val in form.cleaned_data.iteritems():
            key = form.fields[field].label  # use form display label when available
            if key is None:     # if field label is not set, use field name as a fall-back
                key = field 
            if val:     # if search value is not empty, selectively add it
                if field == 'collection':       # for collections, get collection info
                    search_info[key] = get_cached_collection_dict(val)
                elif val != form.fields[field].initial:     # ignore default values
                    search_info[key] = val
        ctx_dict['search_info'] = search_info

        if search_opts:
            # If they didn't specify any search options, don't bother
            # searching.
            try:
                repo = Repository(request=request)
                found = repo.find_objects(**search_opts)
                paginator = Paginator(list(found), 30)

                try:
                    page = int(request.GET.get('page', '1'))
                except ValueError:
                    page = 1
                try:
                    results = paginator.page(page)
                except (EmptyPage, InvalidPage):
                    results = paginator.page(paginator.num_pages)

                ctx_dict['results'] = results.object_list
                ctx_dict['page'] = results
                # pass search term query opts to view for pagination links
                ctx_dict['search_opts'] = request.GET.urlencode()
            except:
                response_code = 500
                ctx_dict['server_error'] = 'There was an error ' + \
                    'contacting the digital repository. This ' + \
                    'prevented us from completing your search. If ' + \
                    'this problem persists, please alert the ' + \
                    'repository administrator.'

    response = render_to_response('audio/search.html', ctx_dict,
                    context_instance=RequestContext(request))
    if response_code is not None:
        response.status_code = response_code
    return response

@permission_required('is_staff')
def view(request, pid):
    '''View a single :class:`~keep.audio.models.AudioObject`.
    Not yet implemented; for now, redirects to :meth:`edit` view.
    '''
    # this view isn't implemented yet, but we want to be able to use the
    # uri. so if someone requests the uri, send them straight to the edit
    # page for now.
    return HttpResponseSeeOtherRedirect(reverse('audio:edit',
                kwargs={'pid': pid}))

@permission_required('is_staff')
def raw_datastream(request, pid, dsid):
    'Access raw object datastreams (mods, rels-ext, dc, digitaltech, sourcetech)'
    repo = Repository(request=request)
    obj = repo.get_object(pid, type=AudioObject)
    dsid = dsid.replace('-', '_')   # convert url dsid to datastream variable form
    try:
        # NOTE: could test that pid is actually an AudioObject using
        # obj.has_requisite_content_models but that would mean
        # an extra API call for every datastream but RELS-EXT
        # Leaving out for now, for efficiency
        ds = getattr(obj, dsid)
        if ds.exists:
            return HttpResponse(ds.content.serialize(pretty=True), mimetype=ds.mimetype)
        else:
            raise Http404
    except RequestFailed as rf:
        # if not actually an AudioObject or if either the object
        # or the requested datastream doesn't exist, 404
        if rf.code == 404 or not obj.has_requisite_content_models or \
                not obj.exists or not obj.dsid.exists:
            raise Http404

        # for anything else, re-raise & let Django's default 500 logic handle it
        raise

@permission_required('is_staff')
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
                obj.save()
                messages.success(request, 'Updated %s' % pid)
                # save & continue functionality - same as collection edit
                if '_save_continue' not in request.POST:
                    return HttpResponseSeeOtherRedirect(reverse('audio:index'))
                # otherwise - fall through to display edit form again
        else:
            # GET - display the form for editing, pre-populated with content from the object
            form = audioforms.AudioObjectEditForm(instance=obj)

        return render_to_response('audio/edit.html', {'obj' : obj, 'form': form },
            context_instance=RequestContext(request))

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
        
         
@permission_required('is_staff')
def download_audio(request, pid):
    "Serve out the audio datastream for the fedora object specified by pid."
    repo = Repository(request=request)
    obj = repo.get_object(pid, type=AudioObject)
    # NOTE: this will probably need some work to be able to handle large datastreams
    try:
        response = HttpResponse(obj.audio.content, mimetype=obj.audio.mimetype)
        response['Content-Disposition'] = "attachment; filename=%s.wav" % slugify(obj.label)
        return response
    except:
        msg = 'There was an error contacting the digital repository. ' + \
              'This prevented us from accessing audio data. If this ' + \
              'problem persists, please alert the repository ' + \
              'administrator.'
        return HttpResponse(msg, mimetype='text/plain', status=500)

# download audio must be accessed by kiosk - should be IP restricted at apache level
def download_compressed_audio(request, pid):
    "Serve out the compressed audio datastream for the fedora object specified by pid."
    try:
        repo = Repository(request=request)
        obj = repo.get_object(pid, type=AudioObject)
    
        #Check that the stream has been added.
        if(obj.compressed_audio.exists):
            # NOTE: this will probably need some work to be able to handle large datastreams
        
            response = HttpResponse(obj.compressed_audio.content, mimetype=obj.compressed_audio.mimetype)
            response['Content-Disposition'] = "attachment; filename=%s.mp3" % slugify(obj.label)
            return response
        #if the compressed stream has not been added, ie. it conversion not done.
        msg = '<div style="width:800px; font-size:16px;">The compressed audio stream does not currently exist. ' + \
                  'This likely means the the audio conversion process ' + \
                  'for this file is in progress or has failed. Please ' + \
                  'try again shortly, and if the problem persists, contact ' + \
                  'an adminstrator.<br /><br /> To return to the previous ' + \
                  'page, please <a href="javascript:history.go(-1);">[click here]</a>.</div>' 
        return HttpResponse(msg, mimetype='text/html', status=404)
    except:
        msg = 'There was an error contacting the digital repository. ' + \
              'This prevented us from accessing audio data. If this ' + \
              'problem persists, please alert the repository ' + \
              'administrator.'
        return HttpResponse(msg, mimetype='text/plain', status=500)

@permission_required('is_staff')
def feed_list(request):
    'List and link to all current iTunes podcast feeds based on number of objects/pages.'
    paginated_objects = Paginator(list(AudioObject.all()), settings.MAX_ITEMS_PER_PODCAST_FEED)
    return render_to_response('audio/feed_list.html', {
                'per_page': settings.MAX_ITEMS_PER_PODCAST_FEED,
                'pages': paginated_objects.page_range,
                }, context_instance=RequestContext(request))
