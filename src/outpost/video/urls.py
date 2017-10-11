from django.conf.urls import (
    include,
    url,
)

from . import views

nginx = [
    url(
        r'^publish/$',
        views.PublishView.as_view(),
        name='publish'
    ),
    url(
        r'^done/$',
        views.PublishDoneView.as_view(),
        name='done'
    ),
]
recording = [
    url(
        r'^$',
        views.RecordingListView.as_view(),
        name='list'
    ),
    url(
        r'^(?P<pk>\d+)$',
        views.RecordingDetailView.as_view(),
        name='detail'
    ),
    url(
        r'^(?P<pk>\d+)/(?P<exporter>\w+)/$',
        views.RecordingExportView.as_view(),
        name='export'
    ),
]
recorder = [
    url(
        r'^$',
        views.RecorderListView.as_view(),
        name='list'
    ),
    url(
        r'^(?P<pk>\d+)$',
        views.RecorderDetailView.as_view(),
        name='detail'
    ),
    url(
        r'^(?P<pk>\d+)/epiphan/channel/(?P<channel>\d+)/$',
        views.EpiphanChannelView.as_view(),
        name='epiphan-channel'
    ),
]

urlpatterns = [
    url(
        r'^recording/',
        include(recording, namespace='recording')
    ),
    url(
        r'^recorder/',
        include(recorder, namespace='recorder')
    ),
    url(
        r'^nginx/',
        include(nginx, namespace='nginx')
    ),
]
