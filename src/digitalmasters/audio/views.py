import magic

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify

from eulcore.django.fedora.server import Repository

from digitalmasters.audio.forms import UploadForm, SearchForm
from digitalmasters.audio.models import AudioObject

allowed_audio_types = ['audio/x-wav']

@permission_required('is_staff')  # sets ?next=/audio/ but does not return back here
def index(request):
    search = SearchForm()
    return render_to_response('audio/index.html', {'search' : search},
            context_instance=RequestContext(request))

@permission_required('is_staff')
def upload(request):
    "Upload a WAV file and create a new fedora object.  Only accepts audio/x-wav."
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
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
                repo = Repository()
                obj = repo.get_object(type=AudioObject)
                obj.label = form.cleaned_data['label']
                obj.dc.content.title = obj.label
                obj.audio.content = uploaded_file  
                obj.save()
                messages.success(request, 'Successfully ingested WAV file %s in fedora as %s.'
                                % (uploaded_file.name, obj.pid))
                return HttpResponseRedirect(reverse('audio:index'))

            # NOTE: uploaded file does not need to be removed because django
            # cleans it up automatically
    else:
        form = UploadForm()
    return render_to_response('audio/upload.html', {'form': form },
                              context_instance=RequestContext(request))
@permission_required('is_staff')
def search(request):
    "Search for fedora objects by pid or title."
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_opts = {}
            if form.cleaned_data['pid']:
                # NOTE: adding wildcard to match all records in an instance
                search_opts['pid__contains'] = "%s*" % form.cleaned_data['pid']
            if form.cleaned_data['title']:
                search_opts['title__contains'] = form.cleaned_data['title']
                
            repo = Repository()
            found = repo.find_objects(**search_opts)
            return render_to_response('audio/search.html', {'results': found, 'search': form},
                    context_instance=RequestContext(request))
    else:
        form = SearchForm()

    return render_to_response('audio/search.html', {'results': found, 'search': form},
                    context_instance=RequestContext(request))
    
@permission_required('is_staff')
def edit(request, pid):
    # place-holder so search results have somewhere to link to
    repo = Repository()
    obj = repo.get_object(pid, type=AudioObject)
    return render_to_response('audio/edit.html', {'obj' : obj },
            context_instance=RequestContext(request))


@permission_required('is_staff')
def download_audio(request, pid):
    "Serve out the audio datastream for the fedora object specified by pid."
    repo = Repository()
    obj = repo.get_object(pid, type=AudioObject)
    # NOTE: this will probably need some work to be able to handle large datastreams
    response = HttpResponse(obj.audio.content, mimetype=obj.audio.mimetype)
    response['Content-Disposition'] = "attachment; filename=%s.wav" % slugify(obj.label)
    return response

