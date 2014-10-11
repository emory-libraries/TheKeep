from django.conf.urls import *
from keep.video import views

urlpatterns = patterns('',
    url(r'^(?P<pid>[^/]+)/$', views.view, name='view')
)