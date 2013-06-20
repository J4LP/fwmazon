from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'checkout.views.options', name='checkout'),
)
