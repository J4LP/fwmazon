from django.conf.urls import patterns, url
from manager.views import ManagerFitCreation, ManagerFitList, ManagerQueue, ManagerOrderAccept, ManagerOrderDetails, ManagerOrderUpdate

urlpatterns = patterns('',
    url(r'^create$', ManagerFitCreation.as_view(), name='manager-create-fit'),
    url(r'^list$', ManagerFitList.as_view(), name='manager-list-fits'),
    url(r'^queue$', ManagerQueue.as_view(), name='manager-queue'),
    url(r'^order/(?P<order_id>\d+)accept$', ManagerOrderAccept.as_view(), name='manager-order-accept'),
    url(r'^order/(?P<order_id>\d+)/update$', ManagerOrderUpdate.as_view(), name='manager-order-update'),
    url(r'^order/(?P<order_id>\d+)$', ManagerOrderDetails.as_view(), name='manager-order-details'),
)
