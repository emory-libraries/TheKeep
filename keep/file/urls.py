from django.conf.urls.defaults import patterns, url
from keep.file import views

urlpatterns = patterns('',
    url(r'^upload/$', views.upload, name='upload'),
)
