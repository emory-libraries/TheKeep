from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': 'audio/', 'permanent' : False}),
    (r'^admin/',  include(admin.site.urls)),
    # NOTE: temporary - added because theme requires it
    url(r'^index$', 'digitalmasters.audio.views.index', name="site-index"),
    url(r'^audio/', include('digitalmasters.audio.urls', namespace='audio')),
    url(r'^accounts/', include('digitalmasters.accounts.urls', namespace='accounts')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)


# DISABLE THIS IN PRODUCTION
if settings.DEV_ENV:
    import os
    # if there's not a genlib_media dir/link in the media directory, then
    # look for it in the virtualenv themes.
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'genlib_media')) and \
            'VIRTUAL_ENV' in os.environ:
        genlib_media_root = os.path.join(os.environ['VIRTUAL_ENV'],
                                         'themes', 'genlib', 'genlib_media')
        urlpatterns += patterns('',
            (r'^static/genlib_media/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': genlib_media_root,
                }),
        )

    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )

