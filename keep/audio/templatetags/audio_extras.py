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
def natural_seconds(seconds):
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
    # only display values that are non-zero
    for dur in ['hour', 'minute', 'second']:
        val = getattr(duration_time, dur)
        if val:
            time_vals.append('%d %s%s' % (val, dur, pluralize(val)))
    return ', '.join(time_vals)





