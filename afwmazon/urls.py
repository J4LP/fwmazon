from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('home.urls')),
    url(r'^manager/', include('manager.urls')),
    url(r'^shop/', include('shop.urls')),
)

