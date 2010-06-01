from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': 'admin/', 'permanent' : False}),
    (r'^admin/',  include(admin.site.urls)),
    # NOTE: temporary - added because theme requires it
    url(r'^index$', 'digitalmasters.audio.views.index', name="site-index"),
    url(r'^audio/', include('digitalmasters.audio.urls', namespace='audio')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)


# DISABLE THIS IN PRODUCTION
if settings.DEV_ENV:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )

