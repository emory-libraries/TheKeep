import operator
from keep.collection.models import CollectionObject, SimpleCollection
from keep.audio.models import AudioObject
from keep.arrangement.models import ArrangementObject
from keep.file.models import DiskImage



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
    return solrq.filter(reduce(operator.or_,
        [solrq.Q(content_model=cm) for cm in searchable_cmodels(user)]))

