"""
Outpost URL Configuration
"""

from django.conf import settings
from django.conf.urls import (
    include,
    url,
)
from django.contrib import admin

urlpatterns = [
    url(
        r'^admin/',
        admin.site.urls
    ),
    url(
        r'^o/',
        include('oauth2_provider.urls', namespace='oauth2_provider')
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
        include('djoser.urls.authtoken')
    ),
    url(
        r'^',
        include('outpost.api.urls')
    ),
    url(
        '^',
        include('django.contrib.auth.urls')
    ),
    url(
        r'^',
        include('outpost.base.urls')
    ),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
