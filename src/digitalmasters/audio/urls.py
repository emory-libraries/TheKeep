from django.conf.urls.defaults import *

urlpatterns = patterns('digitalmasters.audio.views',
    url(r'^$', 'index', name='index'),
    url(r'^upload$', 'upload', name='upload'),
    url(r'^search$', 'search', name='search'),
    url(r'^(?P<pid>[^/]+)/edit$', 'edit', name='edit'),
    url(r'^(?P<pid>[^/]+)/audio$', 'download_audio', name='download-audio'),
    url(r'^collections/new$', 'create_collection', name='new-collection'),
)
