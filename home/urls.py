from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'home.views.home', name='home'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'home/login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
)
