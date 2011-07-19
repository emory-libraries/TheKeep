from django.conf.urls.defaults import *

urlpatterns = patterns('keep.collection.views',
    url(r'^$', 'browse', name='browse'),
    url(r'^new/$', 'edit', name='new'),
    url(r'^search/$', 'search', name='search'),
    url(r'^simple/$', 'simple_browse', name='simple_browse'),
    url(r'^simple/(?P<pid>[^/]+)/edit/$', 'simple_edit', name='simple_edit'),
    url(r'^(?P<pid>[^/]+)/$', 'view', name='view'),
    url(r'^(?P<pid>[^/]+)/edit/$', 'edit', name='edit'),
     url(r'^(?P<pid>[^/]+)/(?P<dsid>(MODS|RELS-EXT|DC))/$',
        'view_datastream', name='raw-ds'),
)