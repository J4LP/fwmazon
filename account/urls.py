from django.conf.urls import patterns, url
from account.views import AccountHomeView, AccountOrdersView, AccountOrderDetailView, AccountOrderCancelView

urlpatterns = patterns(
    '',
    url(r'^$', AccountHomeView.as_view(), name='account'),
    url(r'^orders$', AccountOrdersView.as_view(), name='account-orders'),
    url(r'^order_details/(?P<order_id>\d+)$', AccountOrderDetailView.as_view(), name='account-order-detail'),
    url(r'^orders/cancel/(?P<order_id>\d+)$', AccountOrderCancelView.as_view(), name='account-order-cancel'),
)
