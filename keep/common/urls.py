from django.conf.urls.defaults import *

urlpatterns = patterns('keep.common.views',
        url(r'^search/$', 'search', name='search'),
)