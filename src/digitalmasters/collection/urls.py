from django.conf.urls.defaults import *

urlpatterns = patterns('digitalmasters.collection.views',
    url(r'^$', 'browse', name='browse'),
    url(r'^new$', 'edit', name='new'),
    url(r'^(?P<pid>[^/]+)/edit$', 'edit', name='edit'),
    url(r'^search/$', 'search', name='search'),
    
)
