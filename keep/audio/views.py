import logging

from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from eulcommon.djangoextras.auth import permission_required_with_403, \
    permission_required_with_ajax
from eulcommon.djangoextras.http import HttpResponseSeeOtherRedirect
from eulfedora.views import raw_datastream, raw_audit_trail
from eulfedora.util import RequestFailed, PermissionDenied

from keep.accounts.utils import prompt_login_or_403
from keep.audio import forms as audioforms
from keep.audio.models import AudioObject
from keep.audio.feeds import feed_items
from keep.audio.tasks import queue_access_copy
from keep.common.fedora import Repository, history_view

logger = logging.getLogger(__name__)



def view(request, pid):
    '''View a single :class:`~keep.audio.models.AudioObject`.
    User must either have general view audio permissions, or if they have
    view researcher audio, the object must be researcher accessible
    (based on rights codes).
    '''
    repo = Repository(request=request)
    obj = repo.get_object(pid, type=AudioObject)
    # user either needs view audio permissions OR
    # if they can view researcher audio and object must be researcher-accessible
    if not request.user.has_perm('audio.view_audio') and \
       not (request.user.has_perm('audio.view_researcher_audio') and \
       bool(obj.researcher_access)):
        return prompt_login_or_403(request)

    return render(request, 'audio/view.html', {'resource': obj})


@permission_required_with_403("audio.view_audio")
def view_datastream(request, pid, dsid):
    'Access raw object datastreams (MODS, RELS-EXT, DC, DigitalTech, SourceTech, JHOVE)'
    # initialize local repo with logged-in user credentials & call generic view

    return raw_datastream(request, pid, dsid, type=AudioObject,
                          repo=Repository(request=request))


@permission_required_with_403("audio.view_audio")
def view_audit_trail(request, pid):
    'Access XML audit trail for an audio object'
    # initialize local repo with logged-in user credentials & call eulfedora view
    # FIXME: redundant across collection/arrangement/audio apps; consolidate?
    return raw_audit_trail(request, pid, type=AudioObject,
                           repo=Repository(request=request))


@permission_required_with_403("audio.change_audio")
def edit(request, pid):
    '''Edit the metadata for a single :class:`~keep.audio.models.AudioObject`.'''
    repo = Repository(request=request)
    obj = repo.get_object(pid, type=AudioObject)
    try:
        # if this is not actually an AudioObject, then 404 (object is not available at this url)
        if not obj.has_requisite_content_models:
            raise Http404

        if request.method == 'POST':
            # if data has been submitted, initialize form with request data and object mods
            form = audioforms.AudioObjectEditForm(request.POST, instance=obj)
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
                        (reverse('audio:view', args=[pid]), pid))
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
            form = audioforms.AudioObjectEditForm(instance=obj)

        return render(request, 'audio/edit.html', {'obj': obj, 'form': form})

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
              'This prevented us from accessing audio data. If this ' + \
              'problem persists, please alert the repository ' + \
              'administrator.'
        return HttpResponse(msg, mimetype='text/plain', status=500)


@permission_required_with_403("audio.view_audio")
def history(request, pid):
    return history_view(request, pid, type=AudioObject,
                        template_name='audio/history.html')


# download audio must be accessed by iTunes kiosk - should be IP restricted at apache level
# cannot be restricted to staff only here
# FIXME: enable better controls once we can turn off itunes kiosk
#@permission_required("audio.download_audio")
def download_audio(request, pid, type, extension=None):
    '''Serve out an audio datastream for the fedora object specified by pid.
    Can be used to download original (WAV) audio file or the access copy (MP3).

    :param pid: pid of the :class:`~keep.audio.models.AudioObject` instance
        from which the audio datastream should be returned
    :param type: which audio datastream to return - should be one of 'original'
        or 'access'
    :param extension: optional filename extension for access copy to
        distinguish between different types of access copies (currently MP3 or M4A)

    The :class:`django.http.HttpResponse` returned will have a Content-Disposition
    set to prompt the user to download the file with a filename based on the
    object noid and an appropriate file extension for the type of audio requested.
    '''
    repo = Repository(request=request)
    # retrieve the object so we can use it to set the download filename
    obj = repo.get_object(pid, type=AudioObject)

    # user needs either *play* or *download* permissions
    # - could be any audio or researcher-accessible only, which additionally
    #   requires checking object is researcher-accessible
    # for now, use presence of 'HTTP_RANGE' in request to differentiate
    # jplayer requests from straight downloads
    # NOTE: this would not be too difficult for a savvy user to circumvent
    # (if they know what we are checking), but is intended mainly to prevent
    # unwanted access by staff and researchers in the reading room

    # if http range is present in request, check for play permissions
    # (also requires that request is for access copy, not original)
    if 'HTTP_RANGE' in request.META:
        if not (request.user.has_perm('audio.play_audio') and type == 'access') and \
               not (request.user.has_perm('audio.play_researcher_audio') and \
                    bool(obj.researcher_access) and type == 'access'):
            return prompt_login_or_403(request)

    # otherwise, check for download permissions
    else:
        # user either needs download audio permissions OR
        # if they can download researcher audio and object must be researcher-accessible
        if not request.user.has_perm('audio.download_audio') and \
               not (request.user.has_perm('audio.download_researcher_audio') and \
                    bool(obj.researcher_access)):
            return prompt_login_or_403(request)


    # determine which datastream is requsted & set datastream id & file extension
    if type == 'original':
        dsid = AudioObject.audio.id
        file_ext = 'wav'
    elif type == 'access':
        dsid = AudioObject.compressed_audio.id
        # make sure the requested file extension matches the datastream
        if (obj.compressed_audio.mimetype == 'audio/mp4' and \
           extension != 'm4a') or \
           (obj.compressed_audio.mimetype == 'audio/mpeg' and \
           extension != 'mp3'):
            raise Http404
        file_ext = extension
    else:
        # any other type is not supported
        raise Http404
    extra_headers = {
        'Content-Disposition': "attachment; filename=%s.%s" % (obj.noid, file_ext)
    }
    # use generic raw datastream view from eulfedora
    return raw_datastream(request, pid, dsid, type=AudioObject,
            repo=repo, headers=extra_headers)
    # errors accessing Fedora will fall through to default 500 error handling


@permission_required_with_ajax("audio.generate_audio_access")
@require_http_methods(['POST'])
def tasks(request, pid):
    '''
    Manage tasks associated with an :class:`~keep.audio.models.AudioObject'.
    Currently, the only supported functionality is to queue access
    copy conversion; this should be done by POSTing the type of task to
    be queued, i.e. **generate access copy**.

    Supported tasks:
        * **generate access copy** - queue access copy conversion for an audio
        item by pid.  Returns a status message as the body of a plain/text response

    :param pid: the pid of the object for which tasks should be queued

    '''
    if request.method == 'POST':
        status = "queued"
        task_type = request.POST.get('task', None)

        # TODO May want to prevent queuing of more than one at a time or within a time period.
        # TODO For now javascript disables the link until the page is refreshed.

        # currently the only supported task is
        if task_type == 'generate access copy':
            try:
                repo = Repository(request=request)
                obj = repo.get_object(pid, type=AudioObject)

                # if object doesn't exist or isn't an audio item, 404
                if not obj.exists or not obj.has_requisite_content_models:
                    raise Http404

                queue_access_copy(obj)
                status = 'Successfully queued access copy conversion'

            except Exception as err:
                # re-raise any 404 error
                if isinstance(err, Http404):
                    raise

                logger.error('Error queueing access copy conversion for %s : %s' % \
                    (pid, err))
                status = 'Error queueing access copy conversion (%s)' % err

            return HttpResponse(status, content_type='text/plain')

        # unsupported task
        else:
            return HttpResponse('Task "%s" is not supported' % task_type,
                content_type='text/plain', status=500)
