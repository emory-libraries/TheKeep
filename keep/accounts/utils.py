import operator

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext
from django.template.loader import get_template
from django.utils.http import urlquote

from keep.collection.models import CollectionObject, SimpleCollection
from keep.audio.models import AudioObject
from keep.video.models import Video
from keep.arrangement.models import ArrangementObject
from keep.file.models import DiskImage

import logging
logger = logging.getLogger(__name__)

def searchable_cmodels(user):
    '''Generate a list of content models that can included in search results,
    based on the user's view permissions.

    :param user: instance of :class:`~django.contrib.auth.models.User`
        to use for checking permissions
    :returns: filtered solr query
    '''
    cmodels = []
    if user.has_perm('collection.view_collection'):
        cmodels.append(CollectionObject.COLLECTION_CONTENT_MODEL)
    if user.has_perm('audio.view_audio'):
        cmodels.append(AudioObject.AUDIO_CONTENT_MODEL)
    if user.has_perm('video.view_video'):
        cmodels.append(Video.VIDEO_CONTENT_MODEL)
    if user.has_perm('common.arrangement_allowed'):
        cmodels.append(SimpleCollection.COLLECTION_CONTENT_MODEL)
    if user.has_perm('arrangement.view_arrangement'):
        cmodels.append(ArrangementObject.ARRANGEMENT_CONTENT_MODEL)
        # rushdie file, email message, and email mailbox are all
        # included by using the arrangement content model
    if user.has_perm('file.view_disk_image'):
        cmodels.append(DiskImage.DISKIMAGE_CONTENT_MODEL)


    return cmodels


def filter_by_perms(solrq, user):
    '''Filter a solr query to return only those content models the specified
    user has permission to view.

    :param solrq: sunburnt solr query object
    :param user: instance of :class:`~django.contrib.auth.models.User`
        to use for checking permissions
    :returns: filtered solr query
    '''
    # filter the query with Q(content_model=cm) ORed together for any
    # content models the user has permission to view
    cmodels = searchable_cmodels(user)
    if cmodels:
        solrq = solrq.filter(reduce(operator.or_,
                             [solrq.Q(content_model=cm) for cm in cmodels]))

    # special case filters

    # - only view researcher audio: restrict to audio with appropriate verdict
    if not user.has_perm('audio.view_audio') and \
           user.has_perm('audio.view_researcher_audio'):

        cm_query = solrq.Q(solrq.Q(content_model=AudioObject.AUDIO_CONTENT_MODEL) |
                          solrq.Q(content_model=Video.VIDEO_CONTENT_MODEL))

        solrq = solrq.filter(cm_query).filter(has_access_copy=True, researcher_access=True)
    return solrq


def prompt_login_or_403(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('%s?%s=%s' % (settings.LOGIN_URL,
            REDIRECT_FIELD_NAME, urlquote(request.get_full_path())))
    else:
        tpl = get_template('403.html')
        return HttpResponseForbidden(tpl.render(RequestContext(request)))


