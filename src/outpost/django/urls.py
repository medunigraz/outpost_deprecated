"""
Outpost URL Configuration
"""

from django.conf import settings
from django.conf.urls import (
    include,
    url,
)
from django.contrib import admin
from django.views.static import serve
from rest_framework.authtoken import views as authtoken

urlpatterns = []

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.extend([
        url(
            r'^media/(?P<path>.*)$',
            serve,
            {
                'document_root': settings.MEDIA_ROOT,
            }
        ),
        url(
            r'^static/(?P<path>.*)$',
            serve,
            {
                'document_root': settings.STATIC_ROOT,
            }
        ),
    ])
    urlpatterns.extend([
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ])

urlpatterns.extend([
    url(
        r'^admin/',
        admin.site.urls
    ),
    url(
        r'^auth/api/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
    url(
        r'^prometheus/',
        include('django_prometheus.urls')
    ),
    url(
        r'^auth/token/',
        authtoken.obtain_auth_token
    ),
    url(
        r'^saml2/',
        include('djangosaml2.urls', namespace='saml2')
    ),
    url(
        r'^oauth2/',
        include('outpost.django.oauth2.urls', namespace='oauth2')
    ),
    url(
        r'^attendance/',
        include('outpost.django.attendance.urls', namespace='attendance')
    ),
    url(
        r'^campusonline/',
        include('outpost.django.campusonline.urls', namespace='campusonline')
    ),
    url(
        r'^networktoken/',
        include('outpost.django.networktoken.urls', namespace='networktoken')
    ),
    url(
        r'^typo3/',
        include('outpost.django.typo3.urls', namespace='typo3')
    ),
    url(
        r'^',
        include('outpost.django.api.urls', namespace='api')
    ),
    url(
        r'^',
        include('django.contrib.auth.urls', namespace='accounts')
    ),
    url(
        r'^',
        include('outpost.django.base.urls', namespace='base')
    ),
])
