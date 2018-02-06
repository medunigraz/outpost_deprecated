from django.conf.urls import (
    include,
    url,
)

from . import (
    models,
    views,
)

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
event = [
    url(
        r'^$',
        views.EventListView.as_view(),
        name='list'
    ),
    url(
        r'^create/$',
        views.EventCreateView.as_view(),
        name='create'
    ),
    url(
        r'^(?P<pk>[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12})/$',
        views.EventDetailView.as_view(),
        name='detail'
    ),
    url(
        r'^(?P<pk>[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12})/media/(?:(?P<media>[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12})/)?$',
        views.EventMediaView.as_view(),
        name='media'
    ),
]
publish = [
    url(
        r'^dash/(?P<pk>[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12})/$',
        views.DASHView.as_view(),
        name='dash'
    ),
    url(
        r'^dash/video/(?P<pk>[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12})/(?P<path>.+)$',
        views.DASHMediaView.as_view(model=models.DASHVideoVariant),
        name='dash-video'
    ),
    url(
        r'^dash/audio/(?P<pk>[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12})/(?P<path>.+)$',
        views.DASHMediaView.as_view(model=models.DASHAudio),
        name='dash-audio'
    ),
]

urlpatterns = [
    url(
        r'^event/',
        include(event, namespace='event')
    ),
    url(
        r'^publish/',
        include(publish, namespace='publish')
    ),
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
