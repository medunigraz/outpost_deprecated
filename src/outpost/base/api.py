from django.contrib.contenttypes.models import ContentType

from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from celery.result import AsyncResult
from rest_hooks.models import Hook

from . import models, serializers


class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = serializers.ContentTypeSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    filter_fields = (
        'app_label',
        'model',
    )


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    filter_fields = (
        'object_id',
        'content_type',
    )

    def get_queryset(self):
        if (self.request.user.is_authenticated()):
            return super().get_queryset().filter(user=self.request.user)
        return super().get_queryset().none()


class TaskViewSet(generics.ListAPIView, generics.RetrieveAPIView, viewsets.GenericViewSet):
    serializer_class = serializers.TaskSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        return list()

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        task = self.kwargs[lookup_url_kwarg]
        return AsyncResult(task)


class HookViewSet(viewsets.ModelViewSet):
    """
    Retrieve, create, update or destroy webhooks.
    """
    queryset = Hook.objects.all()
    model = Hook
    serializer_class = serializers.HookSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
