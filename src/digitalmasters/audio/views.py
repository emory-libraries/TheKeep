import magic
import logging
import os
import tempfile
import hashlib
import sys

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify

from eulcore.django.http import HttpResponseSeeOtherRedirect
from eulcore.fedora.util import RequestFailed

from digitalmasters.audio import forms as audioforms
from digitalmasters.audio.models import AudioObject
from digitalmasters.fedora import Repository

from eulcore.fedora.models import DigitalObjectSaveFailure

from digitalmasters.audio.tasks import convertWAVtoMP3

from digitalmasters.audio.utils import md5sum

allowed_audio_types = ['audio/x-wav', 'audio/wav']

@permission_required('is_staff')  # sets ?next=/audio/ but does not return back here
def index(request):
    search = audioforms.ItemSearch()
    return render_to_response('audio/index.html', {'search' : search},
            context_instance=RequestContext(request))

@permission_required('is_staff')
def upload(request):
    "Upload file(s) and create new fedora object(s).  Only accepts audio/x-wav currently."

    ctx_dict = {}
    response_code = None

    if request.method == 'POST':
        #See if it is manual upload due to non-HTML5 browser.
        if request.FILES.has_key('fileManualUpload'):
            uploaded_file = request.FILES['fileManualUpload']
            m = magic.Magic(mime=True)
            type = m.from_file(uploaded_file.temporary_file_path())
            
            if ';' in type:
                type, charset = type.split(';')
            if type not in allowed_audio_types:
                messages.error(request, 'The file uploaded is not of an accepted type (got %s)' % type)
            else:
                try:
                    # initialize from the file itself; use original name as initial object label
                    obj = AudioObject.init_from_file(uploaded_file.temporary_file_path(),
                                                     uploaded_file.name, request, md5sum(uploaded_file.temporary_file_path()))
                    obj.save()
                    #Start the task to convert the WAV audio to a compressed format.
		    convertWAVtoMP3.delay(obj.pid)
                    messages.success(request, 'Successfully ingested file %s in fedora as %s.'
                            % (uploaded_file.name, obj.pid))
                except Exception as e:
                    response_code = 500
                    ctx_dict['server_error'] = 'There was an error ' + \
                            'contacting the digital repository. This ' + \
                            'prevented us from ingesting your file. If ' + \
                            'this problem persists, please alert the ' + \
                            'repository administrator.'
                    response = render_to_response('audio/uploadForm.html', ctx_dict,context_instance=RequestContext(request))
                    if response_code is not None:
                        response.status_code = response_code
                    return response
                    
        #Process the list of files.
        elif request.POST.has_key('fileUploads'):

            file_list = request.POST.getlist('fileUploads')
            file_original_name_list = request.POST.getlist('originalFileNames')
            file_md5sum_list = request.POST.getlist('fileMD5sum')

            if len(file_list) != len(file_original_name_list) != len(file_md5sum_list):
                messages.error(request, 'The hidden input file lists length did not match... some type of form error')
            else:
                for index in range(len(file_list)):
                    #Add the full path qualifier of the temp directory from settings.
                    fullFilePath = os.path.join(settings.INGEST_STAGING_TEMP_DIR,file_list[index])
                    
                    # check mimetype of uploaded file (uploaded_file.content_type is unreliable)
                    m = magic.Magic(mime=True)
                    type = m.from_file(fullFilePath)
                    del m
                    if ';' in type:
                        type, charset = type.split(';')
                    if type not in allowed_audio_types:
                        messages.error(request, 'The file %s is not of an accepted type (got %s)' % (file_original_name_list[index], type))
                    #type is allowed
                    else:
                        #recheck md5sum once more before ingesting....
                        if file_md5sum_list[index] != md5sum(fullFilePath):
                            messages.error(request, 'The file %s has a corrupted MD5 sum on the server.' % file_original_name_list[index])
                        else:
                            #fedora inject code to go here....
                            try:
                                 # initialize from the file itself; use original name as initial object label
                                obj = AudioObject.init_from_file(fullFilePath,
                                                     file_original_name_list[index], 
                                                     request,
                                                     file_md5sum_list[index])
                                obj.save()
                                #Start the task to convert the WAV audio to a compressed format.
				convertWAVtoMP3.delay(obj.pid)
                                messages.success(request, 'Successfully ingested file %s in fedora as %s.'
                                                % (file_original_name_list[index], obj.pid))
                                # clean up temporary upload file after successful ingest
                                os.remove(fullFilePath)
                            except Exception as e:
                                logging.debug(e)
                                messages.error(request, 'Failed to ingest file %s in fedora (fedora is either down or the checksum is incorrect).'
                                               % (file_original_name_list[index]))
                        
        #Return the response with the messages for both cases above.
        return HttpResponseSeeOtherRedirect(reverse('audio:index'))

    #non-posted form
    else:
        ctx_dict['allowed_audio_types'] = allowed_audio_types
        ctx_dict['action_page'] = reverse('audio:HTML5FileUpload')

    response = render_to_response('audio/uploadForm.html', ctx_dict,
                                  context_instance=RequestContext(request))
    if response_code is not None:
        response.status_code = response_code
    return response

@permission_required('is_staff')
def HTML5FileUpload(request):
    """Used for the AJAX HTML5 upload only. Accepts the AJAX request, checks the
    request, uploads the file, returns its end name."""
    
    #Setup the directory for the file upload.
    dir = settings.INGEST_STAGING_TEMP_DIR
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    #Get the header values.
    try:
        fileName = request.META['HTTP_X_FILE_NAME']
        fileMD5 = request.META['HTTP_X_FILE_MD5']
    except Exception as e:
        return HttpResponseBadRequest('Error - missing needed headers (either HTTP-X-FILE-NAME or HTTP-X-FILE-MD5).')
    
    #Returns a Tuple with: "<file_base>", ".", and "<file_extension>"
    fileDetailsTuple = fileName.rpartition('.')
    fileBase = fileDetailsTuple[0]
    fileDot = fileDetailsTuple[1]
    fileExtension = fileDetailsTuple[2]
    
    #returnedMkStemp is a tuple with the name in the 2nd position.
    returnedMkStemp = tempfile.mkstemp(fileDot+fileExtension,fileBase+"_",dir)
    
    destination = open(returnedMkStemp[1], 'wb+')
    destination.write(request.raw_post_data)
    destination.close()
    
    newFileName = os.path.basename(returnedMkStemp[1])
    
    try:
        os.close(returnedMkStemp[0])
        m = magic.Magic(mime=True)
        type = m.from_file(returnedMkStemp[1])

        del m
        if ';' in type:
            type, charset = type.split(';')
        if type not in allowed_audio_types:
            os.remove(returnedMkStemp[1])
            #return HttpResonse('alert(The type ' + type + ' of file ' + fileName + ' is not allowed. That file was rejected.); $("item' + request.META['HTTP_X_FILE_INDEX'] + '").remove();')
            return HttpResponseBadRequest('Error - Incorrect File Type')
    except Exception as e:
        logging.debug(e)
        
    #Check the MD5 sum.
    try:
        if md5sum(returnedMkStemp[1]) != fileMD5:
            return HttpResponseBadRequest('Error - MD5 Did Not Match')
    except Exception as e:
        logging.debug(e)

    return HttpResponse(newFileName)
    
@permission_required('is_staff')
def search(request):
    "Search for fedora objects by pid or title."
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
    # this view isn't implemented yet, but we want to be able to use the
    # uri. so if someone requests the uri, send them straight to the edit
    # page for now.
    return HttpResponseSeeOtherRedirect(reverse('audio:edit',
                kwargs={'pid': pid}))

@permission_required('is_staff')
def edit(request, pid):
    '''Edit the metadata for a single :class:`~digitalmasters.audio.models.AudioObject`.'''
    repo = Repository(request=request)

    try:
        obj = repo.get_object(pid, type=AudioObject)
        try:
        	logging.debug(obj.audio.__dir__)
        except Exception as e:
                logging.debug(e)
        if request.method == 'POST':
            # if data has been submitted, initialize form with request data and object mods
            form = audioforms.AudioObjectEditForm(request.POST, instance=obj)
            if form.is_valid():     # includes schema validation
                # update foxml object with MODS from the form
                form.update_instance()      # instance is reference to mods object
                if obj.mods.content.is_valid():
                    obj.save()
                    # TODO: correct this message (also update unit test that looks for it)
                    messages.success(request, 'Updated MODS for %s' % pid)
                    # save & continue functionality - same as collection edit
                    if '_save_continue' not in request.POST:
                        return HttpResponseSeeOtherRedirect(reverse('audio:index'))
                # otherwise - fall through to display edit form again
        else:
            # GET - display the form for editing, pre-populated with content from the object
            form = audioforms.AudioObjectEditForm(instance=obj)

        return render_to_response('audio/edit.html', {'obj' : obj, 'form': form },
            context_instance=RequestContext(request))

    except RequestFailed:
        # FIXME: should 404 when object is not found
        # eventually we will need better error handling... 
        # this could mean the object doesn't exist OR it exists but has no
        # MODS or even that we couldn't contact the server
        messages.error(request, "Error: failed to load %s MODS for editing" % pid)
        return HttpResponseSeeOtherRedirect(reverse('audio:index'))
         
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

@permission_required('is_staff')
def is_compressed_audio_available(pid):
    "Serve out the compressed audio datastream for the fedora object specified by pid."
    repo = Repository(request=request)
    obj = repo.get_object(pid, type=AudioObject)
    if obj.compressed_audio._content == None:
        return false
    else:
        return true

@permission_required('is_staff')
def download_compressed_audio(request, pid):
    "Serve out the compressed audio datastream for the fedora object specified by pid."
    repo = Repository(request=request)
    obj = repo.get_object(pid, type=AudioObject)
    # NOTE: this will probably need some work to be able to handle large datastreams
    try:
        response = HttpResponse(obj.compressed_audio.content, mimetype=obj.compressed_audio.mimetype)
        response['Content-Disposition'] = "attachment; filename=%s.wav" % slugify(obj.label)
        return response
    except:
        msg = 'There was an error contacting the digital repository. ' + \
              'This prevented us from accessing audio data. If this ' + \
              'problem persists, please alert the repository ' + \
              'administrator.'
        return HttpResponse(msg, mimetype='text/plain', status=500)

@permission_required('is_staff')
def download_compressed_audio(request, pid):
    "Serve out the compressed audio datastream for the fedora object specified by pid."
    repo = Repository(request=request)
    obj = repo.get_object(pid, type=AudioObject)
    # NOTE: this will probably need some work to be able to handle large datastreams
    try:
        response = HttpResponse(obj.compressed_audio.content, mimetype=obj.compressed_audio.mimetype)
        response['Content-Disposition'] = "attachment; filename=%s.mp3" % slugify(obj.label)
        return response
    except:
        msg = 'There was an error contacting the digital repository. ' + \
              'This prevented us from accessing audio data. If this ' + \
              'problem persists, please alert the repository ' + \
              'administrator.'
        return HttpResponse(msg, mimetype='text/plain', status=500)
