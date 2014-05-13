import datetime
from eulfedora.models import DigitalObject
from django import template
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter

from pidservices.clients import parse_ark

from eulcm.models.boda import Arrangement, Mailbox, EmailMessage, RushdieFile

from keep.audio.models import AudioObject
from keep.collection.models import CollectionObject
from keep.common.fedora import user_full_name
from keep.file.models import DiskImage

register = template.Library()

@register.filter
@stringfilter
def ark_id(ark_uri):
    '''Display just the ark identifier (ark:/###/###) given a full
    ARK URI.'''
    try:
        parsed_ark = parse_ark(ark_uri)
        return 'ark:/%(naan)s/%(noid)s' % parsed_ark
    except:
        pass


@register.filter
@stringfilter
def ark_noid(ark_uri):
    '''Display just the NOID (nice opaque identifier) for an ARK given
    a full ARK URI.'''
    try:
        parsed_ark = parse_ark(ark_uri)
        return parsed_ark['noid']
    except:
        pass


@register.filter
@stringfilter
def natural_date(date):
    '''Display human readable date (Feb 01, 2002) for an ISO date in format
    YYYY-MM-DD, YYYY-MM, or YYYY.'''
    date_parts = date.split('-')
    date_parts = [int(v) for v in date_parts]
    # year only: no modification needed
    if len(date_parts) == 1 or date_parts[1] == 0:  # also handle YYYY-00-00
        return '%s' % date_parts[0]
    elif len(date_parts) == 2 or date_parts[2] == 0:
        d = datetime.date(date_parts[0], date_parts[1], 1)
        return d.strftime('%b %Y')
    else:
        d = datetime.date(*date_parts)
        # NOTE: Using 0-padded date because that is only option
        return d.strftime('%b %d, %Y')


@register.filter
@stringfilter
def username_to_name(username):
    '''Return the fullname of a Keep user if they are in the database;
    if not, returns username.  Template tag wrapper around
    :meth:`keep.common.fedora.user_full_name`.'''
    return user_full_name(username)



@register.filter
def view_url(item):
    '''Return the view url for an item.  Supports any model with a
    get_absolute_url method, :class:`~eulfedora.models.DigitalObject`
    subclasses relevant to :mod:`keep`, and Solr results for equivalent
    Keep objects.
    '''

    # if the object knows its own url, use that
    if hasattr(item, 'get_absolute_url'):
        return item.get_absolute_url()

    # get content model - support DigitalObject OR solr result
    if isinstance(item, DigitalObject):
        cmodels = item.get_models()
        pid = item.pid
    else:
        cmodels = item.get('content_model', [])
        pid = item['pid']

    viewname = None
    if AudioObject.AUDIO_CONTENT_MODEL in cmodels:
        viewname = 'audio:view'
    elif DiskImage.DISKIMAGE_CONTENT_MODEL in cmodels:
        viewname = 'file:view'
    elif CollectionObject.COLLECTION_CONTENT_MODEL in cmodels:
        viewname = 'collection:view'

    elif Mailbox.MAILBOX_CONTENT_MODEL in cmodels or \
      EmailMessage.EMAIL_MESSAGE_CMODEL in cmodels:
         viewname = 'arrangement:view'

    elif Arrangement.ARRANGEMENT_CONTENT_MODEL in cmodels or \
      RushdieFile.RUSHDIE_FILE_CMODEL in cmodels:
       #  other objects do not yet have a view url; all arrangement objects use the same edit url
       pass

    if viewname is not None:
        return reverse(viewname, kwargs={'pid': pid})
    else:
        return ''


@register.filter
def edit_url(item):
    '''Return the edit url for an item, if available.  Supports
    :class:`~eulfedora.models.DigitalObject` subclasses relevant to
    :mod:`keep`, and Solr results for equivalent  Keep objects.
    '''

    # get content model - support DigitalObject OR solr result
    if isinstance(item, DigitalObject):
        cmodels = item.get_models()
        pid = item.pid
    else:
        cmodels = item.get('content_model', [])
        pid = item['pid']

    viewname = None
    if AudioObject.AUDIO_CONTENT_MODEL in cmodels:
        viewname = 'audio:edit'
    elif DiskImage.DISKIMAGE_CONTENT_MODEL in cmodels:
        viewname = 'file:edit'
    elif CollectionObject.COLLECTION_CONTENT_MODEL in cmodels:
        viewname = 'collection:edit'

    # mailbox object currently has no edit view
    elif Mailbox.MAILBOX_CONTENT_MODEL in cmodels:
        pass

    # all "arrangement" objects currently use the same edit url
    elif Mailbox.MAILBOX_CONTENT_MODEL in cmodels or \
      EmailMessage.EMAIL_MESSAGE_CMODEL in cmodels or \
      Arrangement.ARRANGEMENT_CONTENT_MODEL in cmodels or \
      RushdieFile.RUSHDIE_FILE_CMODEL in cmodels:
         viewname = 'arrangement:edit'

    if viewname is not None:
        return reverse(viewname, kwargs={'pid': pid})
    else:
        return ''



