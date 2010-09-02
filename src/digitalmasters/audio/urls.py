from django.conf.urls.defaults import *

urlpatterns = patterns('digitalmasters.audio.views',
    url(r'^$', 'index', name='index'),
    url(r'^upload$', 'upload', name='upload'),
    url(r'^search$', 'search', name='search'),
    url(r'^(?P<pid>[^/]+)/edit$', 'edit', name='edit'),
    url(r'^(?P<pid>[^/]+)/audio$', 'download_audio', name='download-audio'),
    url(r'^collections/new$', 'edit_collection', name='new-collection'),
    url(r'^collections/(?P<pid>[^/]+)/edit$', 'edit_collection', name='edit-collection'),
    url(r'^collections/search/$', 'collection_search', name='search-collections'),
    url(r'^collections/$', 'collection_browse', name='browse-collections'),
)
