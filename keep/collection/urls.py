from django.conf.urls import patterns, url
from keep.collection import views

urlpatterns = patterns('',
    url(r'^$', views.list_archives, name='list-archives'),
    url(r'^new/$', views.edit, name='new'),
    url(r'^search/$', views.search, name='search'),
    url(r'^suggest/$', views.collection_suggest, name='suggest'),
    url(r'^simple/$', views.simple_browse, name='simple_browse'),
    url(r'^simple/(?P<pid>[^/]+)/edit/$', views.simple_edit, name='simple_edit'),
    # NOTE: archive must come after so we don't match named views as archive aliases
    url(r'^(?P<archive>[a-z]+)/$', views.browse_archive, name='browse-archive'),
    url(r'^(?P<pid>[^/]+)/$', views.view, name='view'),
    url(r'^(?P<pid>[^/]+)/playlist.json$', views.playlist, name='playlist'),
    url(r'^(?P<pid>[^/]+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<pid>[^/]+)/history/$', views.history, name='history'),
    url(r'^(?P<pid>[^/]+)/(?P<dsid>(MODS|RELS-EXT|DC))/$',
        views.view_datastream, name='raw-ds'),
    url(r'^(?P<pid>[^/]+)/AUDIT/$', views.view_audit_trail, name='audit-trail'),
)
