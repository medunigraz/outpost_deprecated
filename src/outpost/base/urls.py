from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^icon/(?P<pk>[0-9]+)/(?P<color>[0-9a-f]{6})$', views.ColorizedIconView.as_view()),
        url(r'^.*$', views.IndexView.as_view()),
]
