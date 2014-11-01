from django.conf.urls import patterns, include, url
from rest_framework import viewsets, routers
from events import views

urlpatterns = patterns('',
    # Registration of new users
    url(r'^register/$', views.RegistrationView.as_view()),

    # Events endpoint
    url(r'^events/$', views.EventsView.as_view()),
    url(r'^events/(?P<event_id>[0-9]*)$', views.EventsView.as_view()),

    # API authentication
    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
    url(r'^api-auth/', include('rest_framework.urls',\
        namespace='rest_framework')),
)
