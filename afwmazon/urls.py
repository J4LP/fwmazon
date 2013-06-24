from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    url(r'^', include('home.urls')),
    url(r'^manager/', include('manager.urls')),
    url(r'^shop/', include('shop.urls')),
    url(r'^checkout/', include('checkout.urls')),
    url(r'^account/', include('account.urls')),
)
