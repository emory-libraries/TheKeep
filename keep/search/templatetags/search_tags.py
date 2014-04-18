import datetime
from django import template
from django.template.defaultfilters import stringfilter

from pidservices.clients import parse_ark


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


