'''
View methods for creating, editing, searching, and browsing
:class:`~keep.collection.models.CollectionObject` instances in Fedora.
'''
import logging

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

from rdflib.namespace import RDF

from keep.collection.forms import CollectionForm, CollectionSearch, SimpleCollectionEditForm
from keep.collection.models import CollectionObject, get_cached_collection_dict, SimpleCollection
from keep.common.fedora import Repository
from keep.common.rdfns import REPO


logger = logging.getLogger(__name__)

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
        search_opts = {
            'type': CollectionObject,
            # for now, restrict to objects in configured pidspace
            'pid__contains': '%s*' % settings.FEDORA_PIDSPACE,
            # for now, restrict by cmodel in dc:format
            'format': CollectionObject.COLLECTION_CONTENT_MODEL,
        }

        if form.cleaned_data['mss']:
            search_opts['identifier__contains'] = str(form.cleaned_data['mss']) # convert int to string
        if form.cleaned_data['title']:
            search_opts['title__contains'] = form.cleaned_data['title']
        if form.cleaned_data['creator']:
            search_opts['creator__contains'] = form.cleaned_data['creator']
        if form.cleaned_data['collection']:
            search_opts['relation'] = form.cleaned_data['collection']

        # collect non-empty, non-default search terms to display to user on results page
        search_info = {}
        for field, val in form.cleaned_data.iteritems():
            key = form.fields[field].label  # use form display label
            if key is None:     # if field label is not set, use field name as a fall-back
                key = field 
            if val:     # if search value is not empty, selectively add it
                if field == 'collection':       # for collections, get collection info
                    search_info[key] = get_cached_collection_dict(val)
                elif val != form.fields[field].initial:     # ignore default values
                    search_info[key] = val
        context['search_info'] = search_info

        # If no user-specified search terms are entered, find all collections
        try:
            repo = Repository(request=request)
            context['results'] = [get_cached_collection_dict(o.pid)
                                    for o in repo.find_objects(**search_opts) ]
        except RequestFailed:
            response_code = 500
            # FIXME: this is duplicate logic from generic search view
            context['server_error'] = 'There was an error ' + \
                'contacting the digital repository. This ' + \
                'prevented us from completing your search. If ' + \
                'this problem persists, please alert the ' + \
                'repository administrator.'

    response = render_to_response('collection/search.html', context,
                    context_instance=RequestContext(request))
    if response_code is not None:
        response.status_code = response_code
    return response

@permission_required('is_staff')
def browse(request):
    '''Browse :class:`~keep.collection.models.CollectionObject` by
    hierarchy, grouped by top-level collection.
    '''
    response_code = None
    context = {}
    try:
        # retrieve all collections - they will be grouped in the template
        collections = CollectionObject.item_collections()
        collections.sort(key=lambda c: c['collection_label'])
        context['collections'] = collections
    except RequestFailed:
        response_code = 500
        # FIXME: this is duplicate logic from generic search view
        context['server_error'] = 'There was an error ' + \
            'contacting the digital repository. This ' + \
            'prevented us from completing your search. If ' + \
            'this problem persists, please alert the ' + \
            'repository administrator.'

    response = render_to_response('collection/browse.html', context,
                    context_instance=RequestContext(request))
    if response_code is not None:
        response.status_code = response_code
    return response

@permission_required('is_staff')
def view_datastream(request, pid, dsid):
    'Access raw object datastreams (MODS, RELS-EXT, DC)'
    # initialize local repo with logged-in user credentials & call generic view
    return raw_datastream(request, pid, dsid, type=CollectionObject, repo=Repository(request=request))


def simple_edit(request, pid=None):
    ''' Edit an existing Fedora
    :class:`~keep.collection.models.SimpleCollection`.  If a pid is
    specified, attempts to retrieve an existing object.
    '''
    repo = Repository(request=request)

    try:
        obj = repo.get_object(pid=pid, type=SimpleCollection)

        if request.method == 'POST':
            #Update SimpleCollection and associated arrangement objects
            status = request.POST['mods-restrictions_on_access']
            form = SimpleCollectionEditForm(instance=obj)
            (success_count, fail_count) = form.update_objects(status)

            if success_count >= 1 and fail_count == 0: # if all objects were  updated correctly
                messages.success(request, "Successfully Updated %s Item(s)" % (success_count))

                #Now Update the SimpleCollection itself
                obj.mods.content.restrictions_on_access.text = status # Change collection status
                saved = obj.save()
                if not saved:
                    messages.error(request, "Failed To Updated Simple Collection Object")
                    logger.error("Failed to update SimpleCollection %s:%s" % (obj.pid, obj.label))
            else:
                messages.error(request, "Successfully Updated %s Item(s) Failed To Update %s Item(s)" % (success_count, fail_count))




        else:
            #Just Display the form
            form = SimpleCollectionEditForm(instance=obj)

    except RequestFailed, e:
        # if there was a 404 accessing objects, raise http404
        # NOTE: this probably doesn't distinguish between object exists with
        # no MODS and object does not exist at all
        if e.code == 404:
            raise Http404
        # otherwise, re-raise and handle as a common fedora connection error
        else:
            raise

    context = {'form': form}
    if pid is not None:
        context['obj'] = obj

    return render_to_response('collection/simple_edit.html', context,
        context_instance=RequestContext(request))

#find objects with a particular type specified  in the rels-ext and return them as
def _objects_by_type(type_uri, type=None):
    """
    Returns a list of objects with the specified type_uri as objects of the specified type
    :param type_uri: The uri of the type being searched
    :param type: The type of object that should be returned
    """
    repo = Repository()

    pids = repo.risearch.get_subjects(RDF.type, type_uri)
    pids_list = list(pids)

    for pid in pids_list:
        yield repo.get_object(pid=pid, type=type)



def simple_browse(request):

    response_code = None
    try:
        objs = _objects_by_type(REPO.SimpleCollection, SimpleCollection)
        context = {'objs' : objs}
    except RequestFailed:
        response_code = 500
        # FIXME: this is duplicate logic from generic search view
        context['server_error'] = 'There was an error ' + \
            'contacting the digital repository. This ' + \
            'prevented us from completing your search. If ' + \
            'this problem persists, please alert the ' + \
            'repository administrator.'



    response =  render_to_response('collection/simple_browse.html', context,
        context_instance=RequestContext(request))
    if response_code is not None:
        response.status_code = response_code
    return response

