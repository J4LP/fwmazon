from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'shop.views.shop', name='shop'),
    url(r'^details/(?P<fit_id>\d+)$', 'shop.views.shop_details', name='shop-details'),
    url(r'^cart/add$', 'shop.views.cart_add', name='cart-add'),
    url(r'^cart$', 'shop.views.cart_view', name='cart'),
)
