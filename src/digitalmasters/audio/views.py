import magic

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify

from eulcore import xmlmap
from eulcore.django.fedora.server import Repository

from digitalmasters.audio.forms import UploadForm, SearchForm, EditForm
from digitalmasters.audio.models import AudioObject, Mods

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
    form = SearchForm(request.GET)
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
            repo = Repository()
            found = repo.find_objects(**search_opts)
            ctx_dict['results'] = found

    return render_to_response('audio/search.html', ctx_dict,
                    context_instance=RequestContext(request))

@permission_required('is_staff')
def edit(request, pid):
    # place-holder so search results have somewhere to link to
    repo = Repository()
    obj = repo.get_object(pid, type=AudioObject)

    # NOTE: fixture text is just a place-holder until edit form gets glued into
    # the repo object
    
    MODS_TEXT = """<mods:mods xmlns:mods="http://www.loc.gov/mods/v3">
  <mods:titleInfo>
    <mods:title>A simple record</mods:title>
  </mods:titleInfo>
  <mods:typeOfResource>text</mods:typeOfResource>
  <mods:note displayLabel="a general note" type="general">remember to...</mods:note>
  <mods:originInfo>
    <mods:dateCreated keyDate='yes'>2010-06-17T00:00:00.00Z</mods:dateCreated>
  </mods:originInfo>
</mods:mods>
"""
    testobj = xmlmap.load_xmlobject_from_string(MODS_TEXT, Mods)
    print testobj.serialize()
    if request.method == 'POST': # If the form has been submitted...
        form = EditForm(request.POST, instance=testobj) # form bound to the POST data
        if form.is_valid():
            instance = form.update_instance()
            # print instance.serialize()
    else:
        form = EditForm(instance=testobj)
        #form = EditForm()
    
    return render_to_response('audio/edit.html', {'obj' : obj, 'form': form },
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

