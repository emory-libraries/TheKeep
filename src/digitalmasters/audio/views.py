import magic
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify

from eulcore.django.http import HttpResponseSeeOtherRedirect
from eulcore.fedora.util import RequestFailed

from digitalmasters.audio import forms as audioforms
from digitalmasters.audio.models import AudioObject, CollectionObject
from digitalmasters.fedora import Repository

allowed_audio_types = ['audio/x-wav']

@permission_required('is_staff')  # sets ?next=/audio/ but does not return back here
def index(request):
    search = audioforms.SearchForm()
    return render_to_response('audio/index.html', {'search' : search},
            context_instance=RequestContext(request))

@permission_required('is_staff')
def upload(request):
    "Upload a WAV file and create a new fedora object.  Only accepts audio/x-wav."

    ctx_dict = {}
    response_code = None

    if request.method == 'POST':
        form = audioforms.UploadForm(request.POST, request.FILES)
        ctx_dict['form'] = form
        if form.is_valid():
            uploaded_file = request.FILES['audio']

            # check mimetype of uploaded file (uploaded_file.content_type is unreliable)
            m = magic.open(magic.MAGIC_MIME)
            m.load()
            type = m.file(uploaded_file.temporary_file_path())
            if ';' in type:
                type, charset = type.split(';')
            if type not in allowed_audio_types:
                messages.error(request, 'Upload file must be a WAV file (got %s)' % type)
            else:
                try:
                    repo = Repository(request=request)
                    obj = repo.get_object(type=AudioObject)
                    obj.label = form.cleaned_data['label']
                    obj.dc.content.title = obj.mods.content.title = obj.label
                    obj.audio.content = uploaded_file  
                    obj.save()
                    messages.success(request, 'Successfully ingested WAV file %s in fedora as %s.'
                                    % (uploaded_file.name, obj.pid))
                    return HttpResponseSeeOtherRedirect(reverse('audio:index'))
                except:
                    response_code = 500
                    ctx_dict['server_error'] = 'There was an error ' + \
                        'contacting the digital repository. This ' + \
                        'prevented us from ingesting your file. If ' + \
                        'this problem persists, please alert the ' + \
                        'repository administrator.'

            # NOTE: uploaded file does not need to be removed because django
            # cleans it up automatically
    else:

        ctx_dict['form'] = audioforms.UploadForm()
        ctx_dict['HTML5Upload'] = audioforms.HTML5Upload()
    response = render_to_response('audio/uploadForm.html', ctx_dict,
                                  context_instance=RequestContext(request))
    if response_code is not None:
        response.status_code = response_code
    return response


def HTML5FileUpload(request):
    #logging.debug(request.META['HTTP_UPLOADEDFILETYPE'])
    #logging.debug('Work please.')
    #logging.debug(request.POST.get('testing'))
    
    dir = settings.INGEST_STAGING_TEMP_DIR
    fileName = request.META['HTTP_X_FILE_NAME']
    
    #Need to see if exists to prevent over-writes.... currently prepends a number.
    counter = 0
    while (os.path.exists(os.path.join(dir, fileName))):
        counter = counter + 1
        fileName = str(counter) + request.META['HTTP_X_FILE_NAME']
        
    filepath = os.path.join(dir, fileName)
    destination = open(filepath, 'wb+')
    destination.write(request.raw_post_data);
    destination.close()
    
    return HttpResponse(fileName)
    
@permission_required('is_staff')
def search(request):
    "Search for fedora objects by pid or title."
    response_code = None
    form = audioforms.SearchForm(request.GET)
    ctx_dict = {'search': form}
    if form.is_valid():
        search_opts = {}
        if form.cleaned_data['pid']:
            # NOTE: adding wildcard to match all records in an instance
            search_opts['pid__contains'] = "%s*" % form.cleaned_data['pid']
        if form.cleaned_data['title']:
            search_opts['title__contains'] = form.cleaned_data['title']

        if search_opts:
            # If they didn't specify any search options, don't bother
            # searching.
            try:
                repo = Repository(request=request)
                found = repo.find_objects(**search_opts)
                ctx_dict['results'] = list(found)
        
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
def edit(request, pid):
    repo = Repository(request=request)

    try:
        obj = repo.get_object(pid, type=AudioObject)        
        if request.method == 'POST':
            # if data has been submitted, initialize form with request data and object mods
            form = audioforms.EditForm(request.POST, instance=obj.mods.content)
            if form.is_valid():     # includes schema validation
                # update foxml object with MODS from the form
                form.update_instance()      # instance is reference to mods object
                if obj.mods.content.is_valid():
                    obj.save()
                    messages.success(request, 'Updated MODS for %s' % pid)
                    return HttpResponseSeeOtherRedirect(reverse('audio:index'))
                # otherwise - fall through to display edit form again
        else:
            # GET - display the form for editing, pre-populated with MODS content from the object
            form = audioforms.EditForm(instance=obj.mods.content)

        return render_to_response('audio/edit.html', {'obj' : obj, 'form': form },
            context_instance=RequestContext(request))

    except:
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
def edit_collection(request, pid=None):
    "Create a new or edit an existing Fedora Collection object with MODS metadata."
    repo = Repository(request=request)
    try:
        # get collection object - existing if pid specified, or new if not
        obj = repo.get_object(type=CollectionObject, pid=pid)
        # NOTE: on new objects, for now, this will generate and throw away pids
        # TODO: solve this in eulcore.fedora before we start using ARKs for pids

        if request.method == 'POST':
            # if data has been submitted, initialize form with request data and object mods
            form = audioforms.CollectionForm(request.POST, instance=obj)
            if form.is_valid():     # includes schema validation
                form.update_instance() # update instance MODS & RELS-EXT (possibly redundant)
                if pid is None:
                    # new object
                    log_message = 'Creating new collection'
                    action = 'Created new'
                else:
                    # existing object
                    log_message = 'Updating collection'
                    action = 'Updated'

                # NOTE: by sending a log message, we force Fedora to store an
                # audit trail entry for object creation, which doesn't happen otherwise
                obj.save(log_message)
                messages.success(request, '%s collection %s' % (action, obj.pid))
                # submit via normal save
                if '_save_continue' not in request.POST:
                    return HttpResponseSeeOtherRedirect(reverse('audio:index'))
                # could also be _save_continue
                # -- fall through and display form; will display save message
            # in any other case - fall through to display edit form again
        else:
            # GET - display the form for editing
            # FIXME: special fields not getting set!
            form = audioforms.CollectionForm(instance=obj)
    except RequestFailed, e:
        # if there was a 404 accessing object MODS, raise http404
        # NOTE: this probably doesn't distinguish between object exists with
        # no MODS and object does not exist at all
        if e.code == 404:
            raise Http404
        # otherwise, re-raise and handle as a common fedora connection error
        else:
            raise e

    context = {'form': form}
    if pid is not None:
        context['collection'] = obj

    return render_to_response('audio/edit_collection.html', context,
        context_instance=RequestContext(request))



@permission_required('is_staff')
def collection_search(request):
    "Search for collection objects."
    response_code = None
    form = audioforms.CollectionSearch(request.GET)
    context = {'search': form}
    if form.is_valid():
        search_opts = {
            'type': CollectionObject,
            # for now, restrict to objects in configured pidspace
            'pid__contains': '%s*' % settings.FEDORA_PIDSPACE,
            # for now, restrict by cmodel in dc:format
            'format': CollectionObject.COLLECTION_CONTENT_MODEL,
        }

        if form.cleaned_data['mss']:
            # NOTE: adding wildcard to match all records in an instance
            search_opts['identifier__contains'] = "%s*" % form.cleaned_data['mss']
        if form.cleaned_data['title']:
            search_opts['title__contains'] = form.cleaned_data['title']
        if form.cleaned_data['creator']:
            search_opts['creator__contains'] = form.cleaned_data['creator']
        if form.cleaned_data['collection']:
            search_opts['relation'] = form.cleaned_data['collection']

        # If no user-specified search terms are entered, find all collections
        try:
            repo = Repository(request=request)
            found = repo.find_objects(**search_opts)
            context['results'] = list(found)
        except:
            response_code = 500
            # FIXME: this is duplicate logic from generic search view
            context['server_error'] = 'There was an error ' + \
                'contacting the digital repository. This ' + \
                'prevented us from completing your search. If ' + \
                'this problem persists, please alert the ' + \
                'repository administrator.'

    response = render_to_response('audio/collection_search.html', context,
                    context_instance=RequestContext(request))
    if response_code is not None:
        response.status_code = response_code
    return response

@permission_required('is_staff')
def collection_browse(request):
    "Browse collections by hierarchy."  
    response_code = None
    context = {}
    try:
        context['collections'] = CollectionObject.top_level()
    except:
        response_code = 500
        # FIXME: this is duplicate logic from generic search view
        context['server_error'] = 'There was an error ' + \
            'contacting the digital repository. This ' + \
            'prevented us from completing your search. If ' + \
            'this problem persists, please alert the ' + \
            'repository administrator.'

    response = render_to_response('audio/collection_browse.html', context,
                    context_instance=RequestContext(request))
    if response_code is not None:
        response.status_code = response_code
    return response