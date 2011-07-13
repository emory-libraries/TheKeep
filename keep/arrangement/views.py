# Create your views here.
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseForbidden, \
    HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext

from keep.common.fedora import Repository
from keep.arrangement import forms as arrangementforms
from keep.arrangement.models import ArrangementObject

def index(request):
    # pass dates in to the view to link to searches for recently uploaded files
    pid = "emory-steven:test"
    repo = Repository(request=request)
    obj = repo.get_object(pid, type=ArrangementObject, create=True)
    form = arrangementforms.ArrangementObjectEditForm(instance=obj)

    return render_to_response('arrangement/edit.html', {'obj' : obj, 'form': form },
        context_instance=RequestContext(request))

def view_datastream(request, pid, dsid):
    'Access raw object datastreams'
    # initialize local repo with logged-in user credentials & call generic view
    return raw_datastream(request, pid, dsid, type=ArrangementObject, repo=Repository(request=request))
