from django.conf.urls.defaults import *
from keep.audio.feeds import PodcastFeed

urlpatterns = patterns('keep.audio.views',
    url(r'^$', 'index', name='index'),
    url(r'^upload/$', 'upload', name='upload'),
    url(r'^search/$', 'search', name='search'),
    url(r'^feeds/$', 'feed_list', name='feed-list'),
    url(r'^feeds/(?P<page>[0-9]+)/$', PodcastFeed(), name='podcast-feed'),
    url(r'^(?P<pid>[^/]+)/$', 'view', name='view'),
    url(r'^(?P<pid>[^/]+)/edit/$', 'edit', name='edit'),
    url(r'^(?P<pid>[^/]+)/(?P<dsid>(MODS|RELS-EXT|DC|DigitalTech|SourceTech))/$',
            'view_datastream', name='raw-ds'),
    url(r'^(?P<pid>[^/]+)/original/$', 'download_audio', {'type': 'original'},
            name='download-audio'),
    # NOTE: access copy filename extension is required for inclusion in iTunes
    url(r'^(?P<pid>[^/]+)/access.mp3$', 'download_audio', {'type': 'access'},
            name='download-compressed-audio'),
)
