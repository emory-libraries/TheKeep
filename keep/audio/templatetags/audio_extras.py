import datetime
from django import template

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


    

        
