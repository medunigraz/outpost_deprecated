from django.conf.urls import url

from . import views

urlpatterns = [
        url(
            r'^avatar/(?P<hash>[\w\d]+)$',
            views.PrivateAvatarView.as_view(),
            name='avatar-private'
        ),
]
