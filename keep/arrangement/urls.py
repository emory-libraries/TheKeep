from django.conf.urls.defaults import *

urlpatterns = patterns('keep.arrangement.views',
    url(r'^(?P<pid>[^/]+)/edit/$', 'index', name='index'),
    url(r'^ds/(?P<pid>[^/]+)/(?P<dsid>(FileTech|Rights))/$',
            'view_datastream', name='raw-ds'),
)
