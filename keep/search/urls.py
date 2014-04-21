from django.conf.urls import patterns, url
from keep.search import views

urlpatterns = patterns('',
    url(r'^$', views.search, name='keyword'),
)
