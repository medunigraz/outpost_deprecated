"""
Outpost URL Configuration
"""

from django.conf import settings
from django.conf.urls import (
    include,
    url,
)
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = []

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.extend(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
    urlpatterns.extend([
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ])

urlpatterns.extend([
    url(
        r'^admin/uwsgi/',
        include('django_uwsgi.urls')
    ),
    url(
        r'^admin/',
        admin.site.urls
    ),
    url(
        r'^auth/api/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
    url(
        r'^auth/token/',
        include('djoser.urls')
    ),
    url(
        r'^auth/',
        include('djoser.urls.authtoken', namespace='djoser')
    ),
    url(
        r'^oauth2/',
        include('outpost.oauth2.urls', namespace='oauth2')
    ),
    url(
        r'^attendance/',
        include('outpost.attendance.urls', namespace='attendance')
    ),
    url(
        r'^video/',
        include('outpost.video.urls', namespace='video')
    ),
    url(
        r'^',
        include('outpost.api.urls', namespace='api')
    ),
    url(
        r'^',
        include('django.contrib.auth.urls', namespace='accounts')
    ),
    url(
        r'^',
        include('outpost.base.urls', namespace='base')
    ),
])
