from celery.result import AsyncResult
from django.http import (
    HttpResponse,
    JsonResponse,
)
from django.shortcuts import get_object_or_404
from django.views.generic import (
    TemplateView,
    View,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    AllowAny,
    DjangoModelPermissions,
    DjangoModelPermissionsOrAnonReadOnly,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.filters import DjangoFilterBackend

from . import models, serializers


class IndexView(TemplateView):
    template_name = 'outpost/index.html'


class ColorizedIconView(View):

    def get(self, request, pk, color):
        icon = get_object_or_404(models.Icon, pk=pk)
        response = HttpResponse(content_type='image/png')
        image = icon.colorize(color)
        image.save(response, 'PNG')
        return response


class TaskView(View):

    def get(self, request, task):
        result = AsyncResult(task)
        return JsonResponse(
            {
                'state': result.state,
                'info': result.info
            }
        )


class NotificationViewSet(ModelViewSet):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_fields = (
        'object_id',
        'content_type',
    )

    def get_queryset(self):
        if (self.request.user.is_authenticated()):
            return super().get_queryset().filter(user=self.request.user)
        return super().get_queryset().none()


class Template404View(TemplateView):
    template_name = 'outpost/404.html'


class Template500View(TemplateView):
    template_name = 'outpost/500.html'
