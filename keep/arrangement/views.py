# Create your views here.
import logging

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from eulcommon.djangoextras.http import HttpResponseSeeOtherRedirect
from eulcommon.searchutil import pages_to_show
from eulcm.models import boda
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
        obj = repo.get_object(pid)
        if request.method == 'POST':
            # if data has been submitted, initialize form with request data and object mods
            form = arrangementforms.ArrangementObjectEditForm(request.POST, files=request.FILES, instance=obj)
            if form.is_valid():
                form.update_instance()
                if form.cleaned_data.get('comment', None):
                    comment = form.cleaned_data['comment']
                else:
                    # NOTE: we could put this in the comment field as the default/initial value...
                    comment = "update metadata"

                obj.save(comment)
                messages.success(request, 'Successfully updated arrangement <a href="%s">%s</a>' % \
                            (reverse('arrangement:edit', args=[obj.pid]), obj.pid))

                # form submitted via normal save button - redirect to arrangement index (currently site index)
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
    only_fields = ['id', 'did__unittitle', 'subseries', 'eadid']
    search_fields = {'eadid': finding_aid_id}
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
                  {'obj': obj, 'form': form, 'series_data': series_data})


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
    only_fields = ['id', 'did__unittitle', 'subseries', 'eadid']
    search_fields = {'eadid': finding_aid_id}
    series_match_fields = {'id': id, 'subseries__id': id, 'subseries__subseries__id': id}
    queryset = Series.objects.also(*return_fields).only(*only_fields).or_filter(**series_match_fields).filter(**search_fields)

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
def view_item(request, pid):
    '''
    Display information about a single object.  Currently
    only supports :class:`eulcm.models.boda.EmailMessage`
    and :class:`eulcm.models.boda.Mailbox` objects.

    :param pid: The pid of the object to be displayed.
    '''

    repo = TypeInferringRepository(request=request)
    obj = repo.get_object(pid)
    context = {'obj': obj}
    if isinstance(obj, boda.EmailMessage):
        template_name = 'arrangement/email_view.html'
    elif isinstance(obj, boda.Mailbox):
        template_name = 'arrangement/mailbox_view.html'

        # use Solr to find paginated messages in this mailbox
        solr = solr_interface()
        q = solr.query(isPartOf=obj.uri)
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
        # add paginated messages to context
        context.update({
            'page': results,
            'show_pages': show_pages,
            'search_opts': request.GET.urlencode()
        })
    else:
        raise Http404

    return render(request, template_name, context)
