from django.shortcuts import render
from django.http import Http404

from keep.common.fedora import Repository, TypeInferringRepository
from keep.video.models import Video
from keep.common.fedora import history_view
from eulfedora.views import raw_datastream, raw_audit_trail



def view(request, pid):
    '''View a single :class:`~keep.video.models.Video`.
    User must either have general view vidoe permissions, or if they have
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
