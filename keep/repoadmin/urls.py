from django.conf.urls import patterns, url

urlpatterns = ['keep.repoadmin.views',
    url(r'^$', 'dashboard', name="dashboard"),
    url(r'^search/$', 'keyword_search', name='search'),
    url(r'^search/suggest/$', 'keyword_search_suggest', name='suggest'),
]
