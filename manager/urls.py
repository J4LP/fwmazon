from django.conf.urls import patterns, url
from manager.views import ManagerFitCreation, ManagerFitList, ManagerQueue

urlpatterns = patterns('',
    url(r'^create$', ManagerFitCreation.as_view(), name='manager-create-fit'),
    url(r'^list$', ManagerFitList.as_view(), name='manager-list-fits'),
    url(r'^queue$', ManagerQueue.as_view(), name='manager-queue'),
)
