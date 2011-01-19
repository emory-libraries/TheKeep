from django.conf.urls.defaults import *

urlpatterns = patterns('keep.collection.views',
    url(r'^$', 'browse', name='browse'),
    url(r'^new$', 'edit', name='new'),
    url(r'^search/$', 'search', name='search'),
    url(r'^(?P<pid>[^/]+)/$', 'view', name='view'),
    url(r'^(?P<pid>[^/]+)/edit$', 'edit', name='edit'),
)
