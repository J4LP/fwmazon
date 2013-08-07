from django.conf.urls import patterns, include, url
from home.views import *

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^guidelines$', GuidelinesView.as_view(), name='guidelines'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'home/login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
)
