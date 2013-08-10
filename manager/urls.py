from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from fwmazon.decorators import is_contractor, is_manager
from manager.views import *

urlpatterns = patterns('',
    url(r'^create$', login_required(is_manager(ManagerFitCreation.as_view())), name='manager-create-fit'),
    url(r'^list$', login_required(is_manager(ManagerFitList.as_view())), name='manager-list-fits'),
    url(r'^queue$', login_required(is_contractor(ManagerQueue.as_view())), name='manager-queue'),
    url(r'^order/(?P<order_id>\d+)/accept$', login_required(is_contractor(ManagerOrderAccept.as_view())), name='manager-order-accept'),
    url(r'^order/(?P<order_id>\d+)/update$', login_required(is_contractor(ManagerOrderUpdate.as_view())), name='manager-order-update'),
    url(r'^order/(?P<order_id>\d+)$', login_required(is_contractor(ManagerOrder.as_view())), name='manager-order'),
    url(r'^wallet$', login_required(is_manager(ManagerWalletList.as_view())), name='manager-wallets'),
    url(r'^wallet/(?P<wallet_id>\d+)$', login_required(is_manager(ManagerWalletDetails.as_view())), name='manager-wallet-details'),
    url(r'^order$', login_required(is_manager(ManagerOrders.as_view())), name='manager-orders'),
    url(r'^order_data$', login_required(is_manager(ManagerOrdersDataTable.as_view())), name='manager-orders-data'),
    url(r'^contractor$', login_required(is_manager(ManagerContractors.as_view())), name='manager-contractors'),
    url(r'^contractor/(?P<user_id>\d+)$', login_required(is_manager(ManagerContractor.as_view())), name='manager-contractor'),
    url(r'^contractor_data$', login_required(is_manager(ManagerContractorsDataTable.as_view())), name='manager-contractors-data'),
)
