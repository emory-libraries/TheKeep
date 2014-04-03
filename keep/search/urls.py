from django.conf.urls import patterns, url
from keep.search import views

urlpatterns = patterns('',
    url(r'^search/$', views.search, name='keyword'),
)
