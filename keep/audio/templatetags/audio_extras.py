import datetime
from django import template
from django.template.defaultfilters import pluralize

register = template.Library()


@register.filter
def seconds_duration(seconds):
    '''Custom template tag to display integer seconds in HH:MM:SS
    format.'''

    # don't error if we got an empty/invalid value
    if not seconds:
        return ''

    duration = datetime.timedelta(seconds=int(seconds))
    return str(duration)


@register.filter
def natural_seconds(seconds, abbreviate=False):
    '''Custom template tag to display integer seconds as HH hours,
    MM minutes, SS seconds.

    Partially inspired by the filters in :mod:`django.contrib.humanize`.
    '''

    # don't error if we got an empty/invalid value
    if not seconds:
        return ''

    duration = datetime.timedelta(seconds=int(seconds))
    duration_time = datetime.datetime(1, 1, 1) + duration
    time_vals = []

    fields = ['hour', 'minute', 'second']

    # only display values that are non-zero
    if abbreviate:
        labels = {'hour': 'hr', 'minute': 'min', 'second': 'sec'}
    else:
        labels = {'hour': 'hour', 'minute': 'minute', 'second': 'second'}

    for dur in fields:
        val = getattr(duration_time, dur)
        if val:
            time_vals.append('%d %s%s' % (val, labels[dur], pluralize(val)))
    return ', '.join(time_vals)



@register.filter
def natural_seconds_abbrev(seconds):
    return natural_seconds(seconds, abbreviate=True)