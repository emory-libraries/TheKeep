from django.conf.urls import *
from keep.video import views

urlpatterns = patterns('',
    url(r'^(?P<pid>[^/]+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<pid>[^/]+)/$', views.view, name='view'),
    url(r'^(?P<pid>[^/]+)/history/$', views.history, name='history'),
    url(r'^ds/(?P<pid>[^/]+)/(?P<dsid>[a-zA-Z-0-9]+)/$',
        views.view_datastream, name='raw-ds'),
    url(r'^(?P<pid>[^/]+)/AUDIT/$', views.view_audit_trail, name='audit-trail'),
    url(r'^(?P<pid>[^/]+)/original/$', views.download_video, {'type': 'original'},
            name='download-video'),
    url(r'^(?P<pid>[^/]+)/access/$', views.download_video, {'type': 'access'}, name='download-compressed-video')
)