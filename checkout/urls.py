from django.conf.urls import patterns, url
from checkout.views import CheckoutView, PayView

urlpatterns = patterns(
    '',
    url(r'^$', CheckoutView.as_view(), name='checkout'),
    url(r'^pay/(?P<order_id>\d+)$', PayView.as_view(), name='checkout'),
)
