from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^create$', 'manager.views.create', name='create-fit'),
    url(r'^list$', 'manager.views.list_fits', name='list-fits'),
)
