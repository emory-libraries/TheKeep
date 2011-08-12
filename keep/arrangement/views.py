# Create your views here.
import urllib2

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseForbidden, \
    HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

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

#@permission_required('is_staff')
def edit(request, pid):
    # pass dates in to the view to link to searches for recently uploaded files
    #pid = "keep-athom09:steven-test"
    #pid = "scande3:steven-test"
    repo = Repository(request=request)
    obj = repo.get_object(pid, type=ArrangementObject)
    print "HELLO THERE!"
    if request.method == 'POST':
        print "YEAH I POSTED!"
        # if data has been submitted, initialize form with request data and object mods
        form = arrangementforms.ArrangementObjectEditForm(request.POST, instance=obj)
        print form.errors
        if form.is_valid():
            print "FORM WAS VALID!"
            form.update_instance() 
            log_message = 'Updating Arrangement Object from Keep'
            action = 'updated'
            obj.save('Updating Arrangement Object from Keep')
            messages.success(request, 'Successfully %s arrangement <a href="%s">%s</a>' % \
                        (action, reverse('arrangement:edit', args=[obj.pid]), obj.pid))
            
            # form submitted via normal save button - redirect to main audio page
            if '_save_continue' not in request.POST:
                return HttpResponseSeeOtherRedirect(reverse('arrangement:index'))

            # otherwise, form was submitted via "save and continue editing"
            else:
                # creating a new object- redirect to the edit-collection url for the new pid
                if pid is None:
                    return HttpResponseSeeOtherRedirect(reverse('arrangement:edit',
                                                        args=[obj.pid]))

                # if form was valid & object was saved but user has requested
                # "save & continue editing" re-init the form so that formsets
                # will display correctly
                else:
                    form = arrangementforms.ArrangementObjectEditForm(instance=obj)
    
    else:
        form = arrangementforms.ArrangementObjectEditForm(instance=obj)

    return_fields = ['eadid']
    search_fields = {'eadid' : 'rushdie1000'}
    queryset = Series.objects.also(*return_fields).filter(**search_fields)

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

#@permission_required('is_staff')
def view_datastream(request, pid, dsid):
    'Access raw object datastreams'
    # initialize local repo with logged-in user credentials & call generic view
    return raw_datastream(request, pid, dsid, type=ArrangementObject, repo=Repository(request=request))

#@permission_required('is_staff')
@csrf_exempt
def get_selected_series_data(request, id):
    'Access the finding aids EAD'

    return_fields = ['eadid']
    search_fields = {'eadid' : finding_aid_id}
    series_match_fields = {'id' : id, 'subseries__id': id, 'subseries__subseries__id': id}
    queryset = Series.objects.also(*return_fields).or_filter(**series_match_fields).filter(**search_fields)
    series_obj = queryset.get()

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


def shortform_id(id, eadid=None):
    """Calculate a short-form id (without eadid prefix) for use in external urls.
    Uses eadid if available; otherwise, relies on the id delimiter character.
    :param id: id to be shortened
    :param eadid: eadid prefix, if available
    :returns: short-form id
    """
    # if eadid is available, use that (should be the most reliable way to shorten id)
    if eadid:
        id = id.replace('%s_' % eadid, '')
        
    # if eadid is not available, split on _ and return latter portion
    elif ID_DELIMITER in id:
        eadid, id = id.split(ID_DELIMITER)

    # this shouldn't happen -  one of the above two options should work
    else:
        raise Exception("Cannot calculate short id for %s" % id)
    return id
