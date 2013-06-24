from django.conf.urls import patterns, url
from account.views import AccountHomeView

urlpatterns = patterns(
    '',
    url(r'^$', AccountHomeView.as_view(), name='account'),
)
