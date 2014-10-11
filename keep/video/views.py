from django.http import HttpResponse

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

    return HttpResponse("You have reached this page with param %s" % pid)

