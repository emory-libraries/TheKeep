from django.conf import settings

from keep.accounts.models import ResearcherIP

def researcher_no_analytics(request):
    # if researcher no analytics is set, check if this is a configured
    # researcher ip and set a template variable that will
    # allow google analytics to be suppressed
    if settings.RESEARCHER_NO_ANALYTICS:
        ip_addr = request.META.get('REMOTE_ADDR', None)
        if ip_addr is not None:
            researcher_ip = ResearcherIP.objects.filter(ip_address__exact=ip_addr).count()
            if researcher_ip:
                return {
                    'RESEARCHER_NO_ANALYTICS': True
                }
    return {}
