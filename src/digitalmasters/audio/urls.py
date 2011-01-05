from django.conf.urls.defaults import *
from digitalmasters.audio.feeds import PodcastFeed

urlpatterns = patterns('digitalmasters.audio.views',
    url(r'^$', 'index', name='index'),
    url(r'^upload/$', 'upload', name='upload'),
    url(r'^HTML5FileUpload/', 'HTML5FileUpload', name='HTML5FileUpload'),
    url(r'^search/$', 'search', name='search'),
    url(r'^feed/$', PodcastFeed(), name='podcast-feed'),
    url(r'^(?P<pid>[^/]+)/$', 'view', name='view'),
    url(r'^(?P<pid>[^/]+)/edit/$', 'edit', name='edit'),
    url(r'^(?P<pid>[^/]+)/(?P<dsid>(mods|rels-ext|dc|digitaltech|sourcetech))/$',
            'raw_datastream', name='raw-ds'),
    url(r'^(?P<pid>[^/]+)/original/$', 'download_audio', name='download-audio'),
    # NOTE: access copy filename extension is required for inclusion in iTunes
    url(r'^(?P<pid>[^/]+)/access.mp3$', 'download_compressed_audio', name='download-compressed-audio'),
)
