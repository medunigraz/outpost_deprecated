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
        include('djoser.urls.authtoken', namespace='djoser')
    ),
    url(
        r'^',
        include('outpost.api.urls')
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
