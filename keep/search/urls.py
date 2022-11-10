from django.conf.urls import patterns, url
from keep.search import views

urlpatterns = [
    url(r'^$', views.search, name='keyword'),
]
