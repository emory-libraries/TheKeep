from django.conf.urls import *
from keep.audio.feeds import PodcastFeed
from keep.audio import views

urlpatterns = patterns('',
    url(r'^(?P<pid>[^/]+)/tasks/$', views.tasks, name='tasks'),
    url(r'^feeds/$', views.feed_list, name='feed-list'),
    url(r'^feeds/(?P<page>[0-9]+)/$', PodcastFeed(), name='podcast-feed'),
    url(r'^(?P<pid>[^/]+)/$', views.view, name='view'),
    url(r'^(?P<pid>[^/]+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<pid>[^/]+)/history/$', views.history, name='history'),
    url(r'^(?P<pid>[^/]+)/(?P<dsid>(MODS|RELS-EXT|DC|DigitalTech|SourceTech|Rights|JHOVE))/$',
            views.view_datastream, name='raw-ds'),
    url(r'^(?P<pid>[^/]+)/AUDIT/$', views.view_audit_trail, name='audit-trail'),
    url(r'^(?P<pid>[^/]+)/original/$', views.download_audio, {'type': 'original'},
            name='download-audio'),
    # NOTE: access copy filename extension is required for inclusion in iTunes
    url(r'^(?P<pid>[^/]+)/access.(?P<extension>(mp3|m4a))$', views.download_audio,
        {'type': 'access'}, name='download-compressed-audio'),
)
