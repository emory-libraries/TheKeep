'''
View methods for creating, editing, searching, and browsing
:class:`~digitalmasters.collection.models.CollectionObject` instances in Fedora.
'''

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from eulcore.django.http import HttpResponseSeeOtherRedirect
from eulcore.fedora.util import RequestFailed

from digitalmasters.collection.forms import CollectionForm, CollectionSearch
from digitalmasters.collection.models import CollectionObject
from digitalmasters.fedora import Repository

@permission_required('is_staff')
def edit(request, pid=None):
    '''Create a new or edit an existing Fedora
    :class:`~digitalmasters.collection.models.CollectionObject` with MODS
    metadata.    If a pid is specified, attempts to retrieve an existing object.
    Otherwise, creates a new one.
    '''
    repo = Repository(request=request)
    try:
        # get collection object - existing if pid specified, or new if not
        obj = repo.get_object(type=CollectionObject, pid=pid)
        # NOTE: on new objects, for now, this will generate and throw away pids
        # TODO: solve this in eulcore.fedora before we start using ARKs for pids

        if request.method == 'POST':
            # if data has been submitted, initialize form with request data and object mods
            form = CollectionForm(request.POST, instance=obj)
            if form.is_valid():     # includes schema validation
                form.update_instance() # update instance MODS & RELS-EXT (possibly redundant)
                if pid is None:
                    # new object
                    log_message = 'Creating new collection'
                    action = 'Created new'
                else:
                    # existing object
                    log_message = 'Updating collection'
                    action = 'Updated'

                # NOTE: by sending a log message, we force Fedora to store an
                # audit trail entry for object creation, which doesn't happen otherwise
                obj.save(log_message)
                messages.success(request, '%s collection %s' % (action, obj.pid))

                # form submitted via normal save button - redirect to main audio page
                if '_save_continue' not in request.POST:
                    return HttpResponseSeeOtherRedirect(reverse('audio:index'))

                # otherwise, form was submitted via "save and continue editing"
                else:
                    # creating a new object- redirect to the edit-collection url for the new pid
                    if pid is None:
                        return HttpResponseSeeOtherRedirect(reverse('collection:edit',
                                                            args=[obj.pid]))

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
            raise e

    context = {'form': form}
    if pid is not None:
        context['collection'] = obj

    return render_to_response('collection/edit.html', context,
        context_instance=RequestContext(request))

@permission_required('is_staff')
def search(request):
    '''Search for :class:`~digitalmasters.collection.models.CollectionObject`
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
            # NOTE: adding wildcard to match all records in an instance
            search_opts['identifier__contains'] = "%s*" % form.cleaned_data['mss']
        if form.cleaned_data['title']:
            search_opts['title__contains'] = form.cleaned_data['title']
        if form.cleaned_data['creator']:
            search_opts['creator__contains'] = form.cleaned_data['creator']
        if form.cleaned_data['collection']:
            search_opts['relation'] = form.cleaned_data['collection']

        # If no user-specified search terms are entered, find all collections
        try:
            repo = Repository(request=request)
            found = repo.find_objects(**search_opts)
            context['results'] = list(found)
        except:
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
    '''Browse :class:`~digitalmasters.collection.models.CollectionObject` by
    hierarchy, grouped by top-level collection.
    '''
    response_code = None
    context = {}
    try:
        context['collections'] = CollectionObject.top_level()
    except:
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
