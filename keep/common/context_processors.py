from django.conf import settings


def common_settings(request):
    '''Template context processor: add selected setting to context
    so it can be used on any page .'''

    context_extras = {
        'ENABLE_BETA_WARNING': getattr(settings, 'ENABLE_BETA_WARNING', False),
    }

    return context_extras