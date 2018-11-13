from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.TokenCreateView.as_view(), name='create'),
    url(r'^(?P<pk>[\w\d\.]+)/$', views.TokenDetailView.as_view(), name='detail'),
]
