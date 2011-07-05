'''
View methods for creating, editing, searching, and browsing
:class:`~keep.collection.models.CollectionObject` instances in Fedora.
'''

from sunburnt import sunburnt

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from eulcommon.djangoextras.http import HttpResponseSeeOtherRedirect
from eulfedora.views import raw_datastream
from eulfedora.util import RequestFailed

from keep.collection.forms import CollectionForm, CollectionSearch
from keep.collection.models import CollectionObject, get_cached_collection_dict
from keep.common.fedora import Repository

@permission_required('is_staff')
def view(request, pid):
    '''View a single :class:`~keep.collection.models.CollectionObject`.
    Not yet implemented; for now, redirects to :meth:`edit` view.
    '''
    # this view isn't implemented yet, but we want to be able to use the
    # uri. so if someone requests the uri, send them straight to the edit
    # page for now.
    return HttpResponseSeeOtherRedirect(reverse('collection:edit',
                kwargs={'pid': pid}))

@permission_required('is_staff')
def edit(request, pid=None):
    '''Create a new or edit an existing Fedora
    :class:`~keep.collection.models.CollectionObject`.  If a pid is
    specified, attempts to retrieve an existing object.  Otherwise, creates a new one.
    '''
    repo = Repository(request=request)
    try:
        # get collection object - existing if pid specified, or new if not
        obj = repo.get_object(type=CollectionObject, pid=pid)
        # NOTE: on new objects, for now, this will generate and throw away pids
        # TODO: solve this in eulfedora before we start using ARKs for pids

        if request.method == 'POST':
            # if data has been submitted, initialize form with request data and object mods
            form = CollectionForm(request.POST, instance=obj)
            if form.is_valid():     # includes schema validation
                form.update_instance() # update instance MODS & RELS-EXT (possibly redundant)
                if pid is None:
                    # new object
                    log_message = 'Creating new collection'
                    action = 'created'
                else:
                    # existing object
                    log_message = 'Updating collection'
                    action = 'updated'

                # NOTE: by sending a log message, we force Fedora to store an
                # audit trail entry for object creation, which doesn't happen otherwise
                obj.save(log_message)
                messages.success(request, 'Successfully %s collection <a href="%s">%s</a>' % \
                        (action, reverse('collection:edit', args=[obj.pid]), obj.pid))

                # form submitted via normal save button - redirect to main audio page
                if '_save_continue' not in request.POST:
                    return HttpResponseSeeOtherRedirect(reverse('audio:index'))

                # otherwise, form was submitted via "save and continue editing"
                else:
                    # creating a new object- redirect to the edit-collection url for the new pid
                    if pid is None:
                        return HttpResponseSeeOtherRedirect(reverse('collection:edit',
                                                            args=[obj.pid]))

                    # if form was valid & object was saved but user has requested
                    # "save & continue editing" re-init the form so that formsets
                    # will display correctly
                    else:
                        form = CollectionForm(instance=obj)

            # form was posted but not valid
            else:
                # if we attempted to save and failed, add a message since the error
                # may not be obvious or visible in the first screenful of the form
                messages.error(request,
                    '''Your changes were not saved due to a validation error.
                    Please correct any required or invalid fields indicated below and save again.''')

            # in any other case - fall through to display edit form again
        else:
            # GET - display the form for editing
            # FIXME: special fields not getting set!
            form = CollectionForm(instance=obj)
    except RequestFailed, e:
        # if there was a 404 accessing object MODS, raise http404
        # NOTE: this probably doesn't distinguish between object exists with
        # no MODS and object does not exist at all
        if e.code == 404:
            raise Http404
        # otherwise, re-raise and handle as a common fedora connection error
        else:
            raise

    context = {'form': form}
    if pid is not None:
        context['collection'] = obj

    return render_to_response('collection/edit.html', context,
        context_instance=RequestContext(request))

@permission_required('is_staff')
def search(request):
    '''Search for :class:`~keep.collection.models.CollectionObject`
    instances.
    '''
    response_code = None
    form = CollectionSearch(request.GET, prefix='collection')
    context = {'search': form}
    if form.is_valid():
        # include all non-blank fields from the form as search terms
        search_opts = dict((key,val) for key,val in form.cleaned_data.iteritems() if val)
        # restrict to currently configured pidspace and collection content model
        search_opts.update({
            'pid': '%s:*' % settings.FEDORA_PIDSPACE,
            'content_model': CollectionObject.COLLECTION_CONTENT_MODEL,
            })

        # collect non-empty, non-default search terms to display to user on results page
        search_info = {}
        for field, val in form.cleaned_data.iteritems():
            key = form.fields[field].label  # use form display label
            if key is None:     # if field label is not set, use field name as a fall-back
                key = field 
            if val:     # if search value is not empty, selectively add it
                if field == 'collection_id':       # for collections, get collection info
                    search_info[key] = get_cached_collection_dict(val)
                elif val != form.fields[field].initial:     # ignore default values
                    search_info[key] = val
        context['search_info'] = search_info

        solr = sunburnt.SolrInterface(settings.SOLR_SERVER_URL)
        solrquery = solr.query(**search_opts).sort_by('source_id')
        # TODO: eventually, we'll need proper pagination here;
        # for now, set a large max to return everything
        context['results'] = solrquery.paginate(start=0, rows=1000).execute()

    # if the form was not valid, set the current instance of the form
    # as the sidebar form instance to display the error
    else:
        context['collection_search'] = form

    # render search results page; if there was an error, results will be displayed as empty
    return render_to_response('collection/search.html', context,
                              context_instance=RequestContext(request))

@permission_required('is_staff')
def browse(request):
    '''Browse :class:`~keep.collection.models.CollectionObject` by
    hierarchy, grouped by top-level collection.
    '''
    search_opts = {
        'pid': '%s:*' % settings.FEDORA_PIDSPACE,
        'content_model': CollectionObject.COLLECTION_CONTENT_MODEL,
    }
    solr = sunburnt.SolrInterface(settings.SOLR_SERVER_URL)
    solrquery = solr.query(pid='%s:*' % settings.FEDORA_PIDSPACE,
                           content_model=CollectionObject.COLLECTION_CONTENT_MODEL).sort_by('source_id')
    results = solrquery.paginate(start=0, rows=1000).execute()
    return render_to_response('collection/browse.html', {'collections': results},
                    context_instance=RequestContext(request))


@permission_required('is_staff')
def view_datastream(request, pid, dsid):
    'Access raw object datastreams (MODS, RELS-EXT, DC)'
    # initialize local repo with logged-in user credentials & call generic view
    return raw_datastream(request, pid, dsid, type=CollectionObject, repo=Repository(request=request))
