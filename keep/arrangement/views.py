# Create your views here.
import urllib2

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, Http404, HttpResponseForbidden, \
    HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from eulcommon.djangoextras.http import HttpResponseSeeOtherRedirect
from eulfedora.util import RequestFailed

from keep.common.fedora import Repository
from keep.arrangement import forms as arrangementforms
from keep.arrangement.models import ArrangementObject
from keep.common.eadmap import Series

#FIXME: Both of these values are currently hardcoded. The aid_id should
#come from the collection. The url is more difficult - the finding aid
#pidman ARKs do not resolve correctly to series/subseries level. Otherwise,
#could use series.ead.url if the ARKs worked.
finding_aids_url = 'https://findingaids.library.emory.edu/documents/'
finding_aid_id = 'rushdie1000'

def index(request):
    return HttpResponse('Implement me', content_type='text/html')

@permission_required('is_staff')
def edit(request, pid):
    '''Edit view for an arrangement object. Currently, create is not
       supported on this form.

       @param pid: The pid of the object being edited.
       '''
    repo = Repository(request=request)
    try:
        obj = repo.get_object(pid, type=ArrangementObject)
        if request.method == 'POST':
            # if data has been submitted, initialize form with request data and object mods
            form = arrangementforms.ArrangementObjectEditForm(request.POST, instance=obj)
            if form.is_valid():
                form.update_instance() 
                log_message = 'Updating Arrangement Object from Keep'
                action = 'updated'
                # NOTE: by sending a log message, we force Fedora to store an
                # audit trail entry for object creation, which doesn't happen otherwise
                obj.save(log_message)
                messages.success(request, 'Successfully %s arrangement <a href="%s">%s</a>' % \
                            (action, reverse('arrangement:edit', args=[obj.pid]), obj.pid))
            
                # form submitted via normal save button - redirect to main audio page
                if '_save_continue' not in request.POST:
                    return HttpResponseSeeOtherRedirect(reverse('arrangement:index'))

                # otherwise, form was submitted via "save and continue editing"
                else:
                    # if form was valid & object was saved but user has requested
                    # "save & continue editing" re-init the form so that formsets
                    # will display correctly
                    form = arrangementforms.ArrangementObjectEditForm(instance=obj)
    
        else:
            form = arrangementforms.ArrangementObjectEditForm(instance=obj)

    except RequestFailed, e:
        # if there was a 404 accessing object MODS, raise http404
        # NOTE: this probably doesn't distinguish between object exists with
        # no MODS and object does not exist at all
        if e.code == 404:
            raise Http404
        # otherwise, re-raise and handle as a common fedora connection error
        else:
            raise

    # Query for the finding aid information.
    return_fields = ['eadid']
    only_fields = ['id','did__unittitle','subseries', 'eadid']
    search_fields = {'eadid' : finding_aid_id }
    queryset = Series.objects.also(*return_fields).only(*only_fields).filter(**search_fields)

    # Builds an id and value dictionary for the jQuery autocomplete.
    series_data = []
    for series in queryset:
        if(series.subseries):
            for subseries in series.subseries:
                series_data.append({'id': subseries.id, 'value': series.title + ": " + subseries.title})
        else:
            series_data.append({'id': series.id, 'value': series.title})

    series_data = simplejson.dumps(series_data)

    return render_to_response('arrangement/edit.html', {'obj' : obj, 'form': form, 'series_data': series_data},
        context_instance=RequestContext(request))

@permission_required('is_staff')
def view_datastream(request, pid, dsid):
    'Access raw object datastreams'
    # initialize local repo with logged-in user credentials & call generic view
    return raw_datastream(request, pid, dsid, type=ArrangementObject, repo=Repository(request=request))

@permission_required('is_staff')
@csrf_exempt
def get_selected_series_data(request, id):
    '''This is called from a JQuery ajax call. It filters on the passed series/subseries id
       and returns a dictionary containing title, uri, ark, full id, and short id. A bit ugly
       at the moment.

       @param id: The series or subseries id that more data is wanted from.
    '''

    # Query for the finding aid information.
    return_fields = ['eadid']
    only_fields = ['id','did__unittitle','subseries', 'eadid']
    search_fields = {'eadid' : finding_aid_id}
    series_match_fields = {'id' : id, 'subseries__id': id, 'subseries__subseries__id': id}
    queryset = Series.objects.also(*return_fields).only(*only_fields).or_filter(**series_match_fields).filter(**search_fields)
    series_obj = queryset.get()

    # Builds a JSON response of further data. A bit ugly currently.
    series_data = {}
    for series in queryset:
        if(series.subseries):
            for subseries in series.subseries:
                if(subseries.id == id):
                    series_data['series1title'] = subseries.title
                    series_data['series1uri'] = finding_aids_url + finding_aid_id + "/" + series.short_id + "/" + subseries.short_id
                    series_data['series1ark'] = series.eadid.url
                    series_data['series1fullid'] = subseries.id
                    series_data['series1shortid'] = subseries.short_id
                    series_data['series2title'] = series.title
                    series_data['series2uri'] = finding_aids_url + finding_aid_id + "/" + series.short_id
                    series_data['series2ark'] = series.eadid.url
                    series_data['series2fullid'] = series.id
                    series_data['series2shortid'] = series.short_id
        else:
            series_data['series1title'] = series.title
            series_data['series1uri'] = finding_aids_url + finding_aid_id + "/" + series.short_id
            series_data['series1ark'] = series.eadid.url
            series_data['series1fullid'] = series.id
            series_data['series1shortid'] = series.short_id

    series_data = simplejson.dumps(series_data)

    return HttpResponse(series_data, content_type='application/json')
