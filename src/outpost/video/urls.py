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
        views.PublishRTMPView.as_view(),
        name='publish'
    ),
    url(
        r'^done/$',
        views.PublishDoneRTMPView.as_view(),
        name='done'
    ),
]
dash = [
    url(
        r'^(?P<pk>[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12})/$',
        views.DASHView.as_view(),
        name='index'
    ),
    url(
        r'^video/(?P<pk>[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12})/(?P<path>.+)$',
        views.DASHMediaView.as_view(model=models.DASHVideoVariant),
        name='video'
    ),
    url(
        r'^audio/(?P<pk>[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12})/(?P<path>.+)$',
        views.DASHMediaView.as_view(model=models.DASHAudio),
        name='audio'
    ),
]

urlpatterns = [
    url(
        r'^dash/',
        include(dash, namespace='dash')
    ),
    url(
        r'^nginx/',
        include(nginx, namespace='nginx')
    ),
]
