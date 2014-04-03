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
