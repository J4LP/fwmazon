from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from shop.views import *


urlpatterns = patterns('',
    url(r'^$', login_required(ShopView.as_view()), name='shop'),
    url(r'^details/(?P<fit_id>\d+)$', login_required(DoctrineDetailsView.as_view()), name='shop-details'),
    url(r'^cart/add$', login_required(CartAddView.as_view()), name='cart-add'),
    url(r'^cart/update$', login_required(CartUpdateView.as_view()), name='cart-update'),
    url(r'^cart/delete$', login_required(CartDeleteView.as_view()), name='cart-delete'),
    url(r'^cart$', login_required(CartView.as_view()), name='cart'),
)
