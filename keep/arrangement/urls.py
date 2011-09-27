from django.conf.urls.defaults import *

urlpatterns = patterns('keep.arrangement.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<pid>[^/]+)/edit/$', 'edit', name='edit'),
    url(r'^ds/(?P<pid>[^/]+)/(?P<dsid>(FileMasterTech|Rights|MODS|RELS-EXT|DC))/$',
            'view_datastream', name='raw-ds'),
    url(r'^get_selected_series_data/(?P<id>[^/]+)', 'get_selected_series_data', name='get_selected_series_data'),
)
