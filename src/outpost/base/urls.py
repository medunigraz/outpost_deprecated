from django.conf.urls import url

from . import views

urlpatterns = [
        url(
            r'^icon/(?P<pk>[0-9]+)/(?P<color>[0-9a-f]{6})$',
            views.ColorizedIconView.as_view(),
            name='icon'
        ),
        url(
            r'^task/(?P<task>(:?[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}|#))/$',
            views.TaskView.as_view(),
            name='task'
        ),
        url(
            r'^$',
            views.IndexView.as_view()
        ),
]
