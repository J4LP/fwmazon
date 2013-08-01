from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from account.views import *

urlpatterns = patterns(
    '',
    url(r'^$', login_required(AccountHomeView.as_view()), name='account'),
    url(r'^orders$', login_required(AccountOrdersView.as_view()),
        name='account-orders'),
    url(r'^order_details/(?P<order_id>\d+)$', login_required(
        AccountOrderDetailView.as_view()), name='account-order-detail'),
    url(r'^orders/cancel/(?P<order_id>\d+)$', login_required(
        AccountOrderCancelView.as_view()), name='account-order-cancel'),
)
