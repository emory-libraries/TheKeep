from django.conf.urls.defaults import *

urlpatterns = patterns('keep.arrangement.views',
    url(r'^$', 'index', name='index'),
    url(r'^batch/(?P<pid>[^/]+)$', 'batch', name='batch'),
    url(r'^ds/(?P<pid>[^/]+)/(?P<dsid>(FileTech|Rights))/$',
            'view_datastream', name='raw-ds'),
)
