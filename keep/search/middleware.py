
class UnsupportedBrowserMiddleware(object):
    '''Custom middleware to check if the current browser is supported.
    If browser is not supported, adds an *unsupported_browser* flag to
    template context so a warning can be displayed.  (Currently only
    Chrome is supported.)
    '''

    def process_template_response(self, request, response):
        if 'Chrome' not in request.META['HTTP_USER_AGENT']:
            response.context_data['unsupported_browser'] = True

        return response
