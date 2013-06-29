from django.conf.urls import patterns, url
from manager.views import ManagerFitCreation, ManagerFitList, ManagerQueue, ManagerAcceptOrder, ManagerOrderDetails

urlpatterns = patterns('',
    url(r'^create$', ManagerFitCreation.as_view(), name='manager-create-fit'),
    url(r'^list$', ManagerFitList.as_view(), name='manager-list-fits'),
    url(r'^queue$', ManagerQueue.as_view(), name='manager-queue'),
    url(r'^accept/(?P<order_id>\d+)$', ManagerAcceptOrder.as_view(), name='manager-accept-order'),
    url(r'^order/(?P<order_id>\d+)$', ManagerOrderDetails.as_view(), name='manager-order-details'),
)
