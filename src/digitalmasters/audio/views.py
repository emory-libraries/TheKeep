import magic
import os

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from digitalmasters.audio.forms import UploadForm

allowed_audio_types = ['audio/x-wav']

@permission_required('is_staff')  # sets ?next=/audio/ but does not return back here
def index(request):
    return render_to_response('audio/index.html')

@permission_required('is_staff')
def upload(request):
    error = None
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['audio']

            # check mimetype of uploaded file (uploaded_file.content_type is unreliable)
            m = magic.open(magic.MAGIC_MIME)
            m.load()
            type = m.file(uploaded_file.temporary_file_path())
            type, charset = type.split('; ')            
            if type not in allowed_audio_types:
                error = 'Upload file must be a WAV file (got %s)' % type
            else:
                return render_to_response('audio/index.html')

            # NOTE: uploaded file does not need to be removed because django
            # cleans it up automatically
    else:
        form = UploadForm()
    return render_to_response('audio/upload.html', { 'form': form, 'error': error },
                              context_instance=RequestContext(request))
    