from django.conf.urls import patterns, url
from keep.file import views

urlpatterns = patterns('',
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^ingest/$', views.largefile_ingest, name='largefile-ingest'),
    url(r'^(?P<pid>[^/]+)/$', views.view, name='view'),
    url(r'^(?P<pid>[^/]+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<pid>[^/]+)/history/$', views.history, name='history'),
    url(r'^ds/(?P<pid>[^/]+)/(?P<dsid>[a-zA-Z-]+)/$',
        views.view_datastream, name='raw-ds'),
    url(r'^(?P<pid>[^/]+)/AUDIT/$', views.view_audit_trail, name='audit-trail'),
)
