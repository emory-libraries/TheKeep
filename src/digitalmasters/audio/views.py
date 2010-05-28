from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from digitalmasters.audio.forms import UploadForm

@permission_required('is_staff')  # sets ?next=/audio/ but does not return back here
def index(request):
    return render_to_response('audio/index.html')

@permission_required('is_staff')
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        # do form stuff
    else:
        form = UploadForm()
    return render_to_response('audio/upload.html', { 'form': form },
                              context_instance=RequestContext(request))
    