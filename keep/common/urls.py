from django.conf.urls import patterns, url

urlpatterns = ['keep.common.views',
        url(r'^search/$', 'search', name='search'),
]