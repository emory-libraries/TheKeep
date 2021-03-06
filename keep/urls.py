from django.conf.urls import patterns, url, include
from django.contrib import admin

# Importing this object is a work-around because eulfedora
# does not load all objects on startup. Once this has been
# changed in eulfedora, this import can be removed.
from keep.arrangement.models import ArrangementObject

admin.autodiscover()

urlpatterns = patterns('',
    (r'^db-admin/',  include(admin.site.urls)),
    url(r'^$', 'keep.search.views.site_index', name="site-index"),

    url(r'^audio/', include('keep.audio.urls', namespace='audio')),
    url(r'^video/', include('keep.video.urls', namespace='video')),
    url(r'^arrangement/', include('keep.arrangement.urls', namespace='arrangement')),
    url(r'^collections/', include('keep.collection.urls', namespace='collection')),
    url(r'^accounts/', include('keep.accounts.urls', namespace='accounts')),
    url(r'^file/', include('keep.file.urls', namespace='file')),
    url(r'^tasks/', include('eulcommon.djangoextras.taskresult.urls', namespace='tasks')),

    # index data for solr
    url(r'^indexdata/', include('eulfedora.indexdata.urls', namespace='indexdata')),

    url(r'^common/', include('keep.common.urls', namespace='common')),

    url(r'^admin/', include('keep.repoadmin.urls', namespace='repo-admin')),

    # possibly put at top-level url?
    url(r'^search/', include('keep.search.urls', namespace='search')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

)
