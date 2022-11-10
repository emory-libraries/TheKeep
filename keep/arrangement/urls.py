from django.conf.urls import patterns, url
from keep.arrangement import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pid>[^/]+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<pid>[^/]+)/history/$', views.history, name='history'),
    url(r'^ds/(?P<pid>[^/]+)/(?P<dsid>(FileMasterTech|Rights|MODS|RELS-EXT|DC|ORIGINAL|CERP|MIME|PDF|provenanceMetadata))/$',
            views.view_datastream, name='raw-ds'),
    url(r'^(?P<pid>[^/]+)/AUDIT/$', views.view_audit_trail, name='audit-trail'),
    url(r'^get_selected_series_data/(?P<id>[^/]+)', views.get_selected_series_data,
        name='get_selected_series_data'),
    url(r'^(?P<pid>[^/]+)/$', views.view_item, name='view'),
]
