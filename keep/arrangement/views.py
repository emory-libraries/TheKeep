# Create your views here.
import logging
import urllib2
from rdflib import URIRef

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, Http404, HttpResponseForbidden, \
    HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from eulcommon.djangoextras.http import HttpResponseSeeOtherRedirect
from eulcommon.searchutil import pages_to_show
from eulfedora.rdfns import model
from eulfedora.util import RequestFailed
from eulfedora.views import raw_datastream, raw_audit_trail

from keep.common.fedora import Repository, history_view, \
     TypeInferringRepository
from keep.common.utils import solr_interface
from keep.arrangement import forms as arrangementforms
from keep.arrangement.models import ArrangementObject
from keep.common.eadmap import Series

logger = logging.getLogger(__name__)

#FIXME: Both of these values are currently hardcoded. The aid_id should
#come from the collection. The url is more difficult - the finding aid
#pidman ARKs do not resolve correctly to series/subseries level. Otherwise,
#could use series.ead.url if the ARKs worked.
finding_aids_url = 'https://findingaids.library.emory.edu/documents/'
finding_aid_id = 'rushdie1000'

@permission_required("common.arrangement_allowed")
def index(request):
    # FIXME/TODO: there is no arrangement index; not sure why this
    # view even exists, but other arrangement views reference it, so
    # leaving at is for now.  Simply redirect to the main site index
    # for now.
    return HttpResponseSeeOtherRedirect(reverse('site-index'))

@permission_required("common.arrangement_allowed")
def edit(request, pid):
    '''
    Edit view for an arrangement object. Currently, create is not
    supported on this form.

    :param pid: The pid of the object being edited.
    '''
    repo = TypeInferringRepository(request=request)
    try:
        # allow to infer type ? 
        obj = repo.get_object(pid)
        if request.method == 'POST':
            # if data has been submitted, initialize form with request data and object mods
            form = arrangementforms.ArrangementObjectEditForm(request.POST, instance=obj)
            if form.is_valid():
                form.update_instance()
                # FIXME: clean up log message handling; use form validation/form data
                if form.comments.cleaned_data.has_key('comment') and form.comments.cleaned_data['comment']:
                    comment = form.comments.cleaned_data['comment']
                else:
                    comment = "update metadata"

                action = 'updated'

                #Add /remove Allowed Restricted Content Models based on status
                # TODO: store these content models in variables that can be referenced/reused
                allowed = (obj.uriref, model.hasModel, URIRef("info:fedora/emory-control:ArrangementAccessAllowed-1.0"))
                restricted = (obj.uriref, model.hasModel,URIRef("info:fedora/emory-control:ArrangementAccessRestricted-1.0"))


                # TODO: this logic has been moved into arrangement
                # object as a pre-save step; test/confirm that it is ok to remove here
                status = request.POST['rights-access']
                if status == "2":
                    if restricted in obj.rels_ext.content:
                        obj.rels_ext.content.remove(restricted)
                    if allowed not in obj.rels_ext.content:
                        obj.rels_ext.content.add(allowed)

                else:
                    if allowed in obj.rels_ext.content:
                        obj.rels_ext.content.remove(allowed)
                    if restricted not in obj.rels_ext.content:
                        obj.rels_ext.content.add(restricted)

                obj.save(comment)
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

    return render(request, 'arrangement/edit.html',
                  {'obj' : obj, 'form': form, 'series_data': series_data})

@permission_required("common.arrangement_allowed")
def view_datastream(request, pid, dsid):
    'Access raw object datastreams'
    # initialize local repo with logged-in user credentials & call generic view
    # use type-inferring repo to pick up rushdie file or generic arrangement
    response = raw_datastream(request, pid, dsid,
                          repo=TypeInferringRepository(request=request))

    # work-around for email MIME data : display as plain text so it
    # can be viewed in the browser
    if response['Content-Type'] == 'message/rfc822':
        response['Content-Type'] = 'text/plain'
    return response

@permission_required("common.arrangement_allowed")
def view_audit_trail(request, pid):
    'Access XML audit trail'
    # initialize local repo with logged-in user credentials & call eulfedora view
    return raw_audit_trail(request, pid, type=ArrangementObject,
                           repo=Repository(request=request))

@permission_required("common.arrangement_allowed")
def history(request, pid):
    'Display human-readable audit trail information.'
    return history_view(request, pid, type=ArrangementObject,
                        template_name='arrangement/history.html')


@permission_required("common.arrangement_allowed")
@csrf_exempt
def get_selected_series_data(request, id):
    '''
    This is called from a JQuery ajax call. It filters on the passed series/subseries id
    and returns a dictionary containing title, uri, ark, full id, and short id. A bit ugly
    at the moment.

    :param id: The series or subseries id that more data is wanted
        from.
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


@permission_required("common.arrangement_allowed")
def email_view(request, pid):
    '''
    View for an EmailMessage object.

    :param pid: The pid of the object.
    '''
    repo = TypeInferringRepository(request=request)
    obj = repo.get_object(pid)

    return render(request, 'arrangement/email_view.html',
                  {'obj' : obj})

@permission_required("common.arrangement_allowed")
def mailbox_view(request, pid):
    '''
    View for an Mailbox object..

    :param pid: The pid of the object.
    '''

    solr = solr_interface()
    q = solr.query(pid=pid).field_limit(['label', 'title', 'hasPart'])
    result = q.execute()
    mailbox = result[0]
    #get title and label from mailbox query
    mailbox_title = mailbox['title']
    mailbox_label = mailbox['label']

    #get labels and pids for each message object
    solr = solr_interface()
    q = solr.query(isPartOf='info:fedora/%s' % pid)

    paginator = Paginator(q, 30)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        results = paginator.page(page)
    except (EmptyPage, InvalidPage):
        results = paginator.page(paginator.num_pages)
    # calculate page links to show
    show_pages = pages_to_show(paginator, page)

    return render(request, 'arrangement/mailbox_view.html',
                  {'title': mailbox_title,
                   'label': mailbox_label,
                   'page': results,
                   'show_pages': show_pages,
                   'search_opts': request.GET.urlencode(),
                  })



