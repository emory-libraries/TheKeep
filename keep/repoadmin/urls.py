from django.conf.urls import patterns, url

urlpatterns = patterns('keep.repoadmin.views',
    url(r'^$', 'keyword_search', name='keyword'),
    url(r'^suggest/$', 'keyword_search_suggest', name='suggest'),
)
