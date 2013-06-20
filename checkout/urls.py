from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'shop.views.checkout', name='checkout'),
)
