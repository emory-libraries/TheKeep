from __future__ import absolute_import

__version_info__ = (2, 7, 2, None)


# Dot-connect all but the last. Last is dash-connected if not None.
__version__ = '.'.join([str(i) for i in __version_info__[:-1]])
if __version_info__[-1] is not None:
    __version__ += ('-%s' % (__version_info__[-1],))


# context processor to add version to the template environment
def version_context(request):
    return {'SW_VERSION': __version__}


# make sure celery app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app
