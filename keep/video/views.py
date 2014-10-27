#TODO add perms for views like in audo

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.contrib import messages
from django.template.response import TemplateResponse
from eulfedora.util import RequestFailed, PermissionDenied
from eulcommon.djangoextras.http import HttpResponseSeeOtherRedirect

from keep.common.fedora import Repository, TypeInferringRepository
from keep.video.models import Video
from keep.video import forms as videoforms
from keep.common.fedora import history_view
from eulfedora.views import raw_datastream, raw_audit_trail

def edit(request, pid):
    '''Edit the metadata for a single :class:`~keep.video.models.Video`.'''
    #*********REMOVE THIS AFTE TEST*********#
    repo = Repository(request=request)
    #repo = Repository(username='fedoraAdmin', password='fedoraAdmin')
    obj = repo.get_object(pid, type=Video)
    try:
        # if this is not actually a Vide0, then 404 (object is not available at this url)
        if not obj.has_requisite_content_models:
            raise Http404

        if request.method == 'POST':
            # if data has been submitted, initialize form with request data and object mods
            form = videoforms.VideoEditForm(request.POST, instance=obj)
            if form.is_valid():     # includes schema validation
                # update foxml object with data from the form
                form.update_instance()      # instance is reference to mods object
                if 'comment' in form.comments.cleaned_data \
                        and form.comments.cleaned_data['comment']:
                    comment = form.comments.cleaned_data['comment']
                else:
                    comment = "update metadata"

                obj.save(comment)
                messages.success(request, 'Successfully updated <a href="%s">%s</a>' % \
                        (reverse('video:view', args=[pid]), pid))
                # save & continue functionality - same as collection edit
                if '_save_continue' not in request.POST:
                    return HttpResponseSeeOtherRedirect(reverse('repo-admin:dashboard'))
                # otherwise - fall through to display edit form again

            # form was posted but not valid
            else:
                # if we attempted to save and failed, add a message since the error
                # may not be obvious or visible in the first screenful of the form
                messages.error(request,
                    '''Your changes were not saved due to a validation error.
                    Please correct any required or invalid fields indicated below and save again.''')

        else:
            # GET - display the form for editing, pre-populated with content from the object
            form = videoforms.VideoEditForm(instance=obj)

        return TemplateResponse(request, 'video/edit.html', {'obj': obj, 'form': form})

    except PermissionDenied:
        # Fedora may return a PermissionDenied error when accessing a datastream
        # where the datastream does not exist, object does not exist, or user
        # does not have permission to access the datastream

        # check that the object exists - if not, 404
        if not obj.exists:
            raise Http404
        # for now, assuming that if object exists and has correct content models,
        # it will have all the datastreams required for this view

        return HttpResponseForbidden('Permission Denied to access %s' % pid,
                                     mimetype='text/plain')

    except RequestFailed as rf:
        # if fedora actually returned a 404, propagate it
        if rf.code == 404:
            raise Http404

        msg = 'There was an error contacting the digital repository. ' + \
              'This prevented us from accessing video data. If this ' + \
              'problem persists, please alert the repository ' + \
              'administrator.'
        return HttpResponse(msg, mimetype='text/plain', status=500)


def view(request, pid):
    '''View a single :class:`~keep.video.models.Video`.
    User must either have general view video permissions, or if they have
    view researcher view, the object must be researcher accessible
    (based on rights codes).
    '''
    # repo = Repository(request=request)
    # obj = repo.get_object(pid, type=AudioObject)
    # # user either needs view audio permissions OR
    # # if they can view researcher audio and object must be researcher-accessible
    # if not request.user.has_perm('audio.view_audio') and \
    #    not (request.user.has_perm('audio.view_researcher_audio') and \
    #    bool(obj.researcher_access)):
    #     return prompt_login_or_403(request)
    #
    # return TemplateResponse(request, 'audio/view.html', {'resource': obj})

    repo = Repository(request=request)
    obj = repo.get_object(pid=pid, type=Video)

    try:
        if not obj.has_requisite_content_models:
            raise Http404
    except:
        raise Http404

    return render(request, 'video/view.html', {"obj": obj})


def history(request, pid):
    'Display human-readable audit trail information.'
    return history_view(request, pid, type=Video, template_name='video/history.html')

def view_audit_trail(request, pid):
    'Access XML audit trail'
    # initialize local repo with logged-in user credentials & call eulfedora view
    # type shouldn't matter for audit trail
    return raw_audit_trail(request, pid, repo=Repository(request=request))


def view_datastream(request, pid, dsid):
    'Access raw object datastreams'
    # initialize local repo with logged-in user credentials & call generic view
    # use type-inferring repo to pick up rushdie file or generic arrangement
    response = raw_datastream(request, pid, dsid,
                          repo=TypeInferringRepository(request=request))

    # work-around for email MIME data : display as plain text so it
    # can be viewed in the browser
    if response.get('Content-Type', None) == 'message/rfc822':
        response['Content-Type'] = 'text/plain'
    return response
