from django.conf.urls import url
from oauth2_provider.views import (
    AuthorizationView,
    TokenView,
)

from .views import ApplicationListView, ApplicationDetailView, ApplicationCreateView, ApplicationEditView, ApplicationDeleteView


urlpatterns = [
    url(
        r'^applications/$',
        ApplicationListView.as_view(),
        name='list'
    ),
    url(
        r'^applications/(?P<pk>\d+)/$',
        ApplicationDetailView.as_view(),
        name='detail'
    ),
    url(
        r'^applications/new/$',
        ApplicationCreateView.as_view(),
        name='create'
    ),
    url(
        r'^applications/(?P<pk>\d+)/edit/$',
        ApplicationEditView.as_view(),
        name='edit'
    ),
    url(
        r'^applications/(?P<pk>\d+)/delete/$',
        ApplicationDeleteView.as_view(),
        name='delete'
    ),
    url(
        r'^authorize/$',
        AuthorizationView.as_view(),
        name='authorize'
    ),
    url(
        r'^token/$',
        TokenView.as_view(),
        name='token'
    ),
]
