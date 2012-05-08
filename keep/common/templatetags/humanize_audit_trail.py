from django import template

register = template.Library()

@register.filter
def humanize_audit_trail(obj):
    '''
    Takes a :class:`~keep.common.fedora.DigitalObject` and returns a list of dicts
    with date/time, user, action  and justification that can be displayed in a human readable format.
    '''

    #according to django docs template tags should fail silently
    try:
        audit_trail =  [{'date': a.date.strftime('%b %d, %Y %I:%M %p'),
                         'user': a.user,
                         'action': a.action,
                         'message': a.message} for a in obj.audit_trail.records]
        audit_trail.reverse() # show the latest entries first
    except:
        audit_trail =""

    return audit_trail

