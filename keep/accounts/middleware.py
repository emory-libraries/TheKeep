from keep.accounts.models import ResearcherIP, AnonymousResearcher


class ResearcherAccessMiddleware(object):

    def process_request(self, request):
        ip_addr = request.META.get('REMOTE_ADDR', None)
        if request.user.is_anonymous() and ip_addr is not None and \
           ResearcherIP.objects.filter(ip_address__exact=ip_addr).exists():
            request.user = AnonymousResearcher()
