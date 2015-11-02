from django.conf.urls import patterns, url
from keep.file import views

urlpatterns = patterns('',
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^ingest/$', views.largefile_ingest, name='largefile-ingest'),
    url(r'^(?P<pid>[^/]+)/$', views.view, name='view'),
    url(r'^(?P<pid>[^/]+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<pid>[^/]+)/supplements/$', views.manage_supplements, name='supplements'),
    url(r'^(?P<pid>[^/]+)/history/$', views.history, name='history'),
    url(r'^ds/(?P<pid>[^/]+)/(?P<dsid>[a-zA-Z-0-9]+)/diff/$',
        views.datastream_diff, name='ds-diff'),
    url(r'^ds/(?P<pid>[^/]+)/(?P<dsid>[a-zA-Z-0-9]+)/diff/full/$',
        views.datastream_diff, {'mode': 'full'}, name='ds-diff-full'),
    url(r'^ds/(?P<pid>[^/]+)/(?P<dsid>[a-zA-Z-0-9]+)/$',
        views.view_datastream, name='raw-ds'),
    url(r'^ds/(?P<pid>[^/]+)/(?P<dsid>[a-zA-Z-0-9]+)/(?P<date>[^/]+)/$',
        views.view_datastream, name='raw-ds-version'),
    url(r'^(?P<pid>[^/]+)/AUDIT/$', views.view_audit_trail, name='audit-trail'),


)
