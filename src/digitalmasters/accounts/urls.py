from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('digitalmasters.accounts.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
)

