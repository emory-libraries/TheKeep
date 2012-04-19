from django.conf.urls.defaults import *

urlpatterns = patterns('keep.search.views',
    url(r'^$', 'keyword_search', name='keyword'),
)
