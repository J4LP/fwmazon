from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'shop.views.shop', name='shop'),
)
