from django.conf.urls import patterns, url

urlpatterns = patterns('keep.common.views',
        url(r'^search/$', 'search', name='search'),
)