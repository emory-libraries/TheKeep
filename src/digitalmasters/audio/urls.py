from django.conf.urls.defaults import *

urlpatterns = patterns('digitalmasters.audio.views',
     url(r'^$', 'index', name='index'),
)
