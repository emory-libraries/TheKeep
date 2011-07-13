from django.conf.urls.defaults import *

urlpatterns = patterns('keep.arrangement.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<pid>[^/]+)/(?P<dsid>(FileTech|Rights))/$',
            'view_datastream', name='raw-ds'),
)
