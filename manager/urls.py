from django.conf.urls import patterns, url
from manager.views import *

urlpatterns = patterns('',
    url(r'^create$', ManagerFitCreation.as_view(), name='manager-create-fit'),
    url(r'^list$', ManagerFitList.as_view(), name='manager-list-fits'),
    url(r'^queue$', ManagerQueue.as_view(), name='manager-queue'),
    url(r'^order/(?P<order_id>\d+)accept$', ManagerOrderAccept.as_view(), name='manager-order-accept'),
    url(r'^order/(?P<order_id>\d+)/update$', ManagerOrderUpdate.as_view(), name='manager-order-update'),
    url(r'^order/(?P<order_id>\d+)$', ManagerOrder.as_view(), name='manager-order'),
    url(r'^wallet$', ManagerWalletList.as_view(), name='manager-wallets'),
    url(r'^wallet/(?P<wallet_id>\d+)$', ManagerWalletDetails.as_view(), name='manager-wallet-details'),
    url(r'^order$', ManagerOrders.as_view(), name='manager-orders'),
    url(r'^order_data$', ManagerOrdersDataTable.as_view(), name='manager-orders-data'),
    url(r'^contractor$', ManagerContractors.as_view(), name='manager-contractors'),
    url(r'^contractor/(?P<user_id>\d+)$', ManagerContractor.as_view(), name='manager-contractor'),
    url(r'^contractor_data$', ManagerContractorsDataTable.as_view(), name='manager-contractors-data'),
)
