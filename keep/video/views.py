from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.contrib import messages
from django.template.response import TemplateResponse
from eulfedora.util import RequestFailed, PermissionDenied
from eulcommon.djangoextras.http import HttpResponseSeeOtherRedirect

from keep.accounts.utils import prompt_login_or_403
from keep.common.fedora import Repository, TypeInferringRepository
from keep.video.models import Video
from keep.video import forms as videoforms
from keep.common.fedora import history_view
from eulfedora.views import raw_datastream, raw_audit_trail
from eulcommon.djangoextras.auth import permission_required_with_403

@permission_required_with_403("video.change_videoperms")
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
    repo = Repository(request=request)
    obj = repo.get_object(pid=pid, type=Video)
    # # user either needs view video permissions OR
    # # if they can view researcher audio and object must be researcher-accessible
    if not request.user.has_perm('video.view_video') and \
       not (request.user.has_perm('video.view_researcher_video') and \
       bool(obj.researcher_access)):
        return prompt_login_or_403(request)

    try:
        if not obj.has_requisite_content_models:
            raise Http404
    except:
        raise Http404


    return render(request, 'video/view.html', {"resource": obj})


@permission_required_with_403("video.view_video")
def history(request, pid):
    'Display human-readable audit trail information.'
    return history_view(request, pid, type=Video, template_name='video/history.html')

@permission_required_with_403("video.view_video")
def view_audit_trail(request, pid):
    'Access XML audit trail'
    # initialize local repo with logged-in user credentials & call eulfedora view
    # type shouldn't matter for audit trail
    return raw_audit_trail(request, pid, repo=Repository(request=request))

@permission_required_with_403("video.view_video")
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


#@permission_required("audio.download_audio")
def download_video(request, pid, type, extension=None):
    '''Serve out an vidoe datastream for the fedora object specified by pid.
    Can be used to download original file or the access copy.

    :param pid: pid of the :class:`~keep.vidoe.models.Video` instance
        from which the vidoe datastream should be returned
    :param type: which video datastream to return - should be one of 'original'
        or 'access'
    :param extension: optional filename extension for access copy to
        distinguish between different types of access copies

    The :class:`django.http.HttpResponse` returned will have a Content-Disposition
    set to prompt the user to download the file with a filename based on the
    object noid and an appropriate file extension for the type of video requested.
    '''
    repo = Repository(request=request)
    # retrieve the object so we can use it to set the download filename
    obj = repo.get_object(pid, type=Video)

    # user needs either *play* or *download* permissions
    # - could be any video or researcher-accessible only, which additionally
    #   requires checking object is researcher-accessible
    # for now, use presence of 'HTTP_RANGE' in request to differentiate
    # jplayer requests from straight downloads
    # NOTE: this would not be too difficult for a savvy user to circumvent
    # (if they know what we are checking), but is intended mainly to prevent
    # unwanted access by staff and researchers in the reading room

    # if http range is present in request, check for play permissions
    # (also requires that request is for access copy, not original)
    if 'HTTP_RANGE' in request.META:
        if not (request.user.has_perm('video.play_video') and type == 'access') and \
               not (request.user.has_perm('video.play_researcher_video') and \
                    bool(obj.researcher_access) and type == 'access'):
            return prompt_login_or_403(request)

    # otherwise, check for download permissions
    else:
        # user either needs download vidoe permissions OR
        # if they can download researcher audio and object must be researcher-accessible
        if not request.user.has_perm('video.download_video') and \
               not (request.user.has_perm('video.download_researcher_video') and \
                    bool(obj.researcher_access)):
            return prompt_login_or_403(request)


    # determine which datastream is requsted & set datastream id & file extension
    if type == 'original':
        dsid = Video.content.id
        file_ext = Video.allowed_master_mimetypes[obj.content.mimetype]
    elif type == 'access':
        dsid = Video.access_copy.id
        # make sure the requested file extension matches the datastream
        file_ext = Video.allowed_access_mimetypes[obj.access_copy.mimetype]
    else:
        # any other type is not supported
        raise Http404
    extra_headers = {
        'Content-Disposition': "attachment; filename=%s.%s" % (obj.noid, file_ext)
    }
    # use generic raw datastream view from eulfedora
    return raw_datastream(request, pid, dsid, type=Video,
            repo=repo, headers=extra_headers, accept_range_request=True)
    # errors accessing Fedora will fall through to default 500 error handling