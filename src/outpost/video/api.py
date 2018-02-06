import json
from pathlib import Path

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    JsonResponse,
)
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy as reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)
from django_downloadview import PathDownloadView
from guardian.shortcuts import get_objects_for_user
from rest_framework.permissions import (
    AllowAny,
    DjangoModelPermissions,
    DjangoModelPermissionsOrAnonReadOnly,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .models import (
    Broadcast,
    Epiphan,
    EpiphanChannel,
    EpiphanSource,
    Event,
    EventAudio,
    EventMedia,
    EventVideo,
    Export,
    Publish,
    DASHPublish,
    DASHAudio,
    DASHVideo,
    Recorder,
    Recording,
    RecordingAsset,
    Stream,
    Token,
)
from .serializers import (
    ExportClassSerializer,
    EventSerializer,
    RecorderSerializer,
    EpiphanSerializer,
    EpiphanChannelSerializer,
    EpiphanSourceSerializer,
    RecordingAssetSerializer,
    RecordingSerializer,
    DASHPublishSerializer,
    DASHAudioSerializer,
    DASHVideoSerializer,
)
from .tasks import ExportTask


class ExportClassViewSet(ListAPIView, RetrieveAPIView, GenericViewSet):
    serializer_class = ExportClassSerializer
    pagination_class = LimitOffsetPagination
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        classes = Export.__subclasses__()
        exporters = [(c.__name__, c._meta.verbose_name) for c in classes]
        return sorted(exporters, key=lambda x: x[0])

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        exporter = self.kwargs[lookup_url_kwarg]
        exporters = dict(self.get_queryset())
        if exporter not in exporters:
            raise Http404('Unknown exporter: {}'.format(exporter))
        return (exporter, exporters.get(exporter))

    def post(self, request, *args, **kwargs):
        exporter = request.data.get('exporter')
        recording = request.data.get('recording')
        task = ExportTask.delay(recording, exporter)
        result = {
            'task': task.id,
        }
        return Response(result)


class RecorderViewSet(ModelViewSet):
    queryset = Recorder.objects.all()
    serializer_class = RecorderSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        DjangoModelPermissions,
    )
    filter_fields = ()

    def get_queryset(self):
        return get_objects_for_user(
            self.request.user,
            'video.view_recorder',
            klass=self.queryset
        )


class RecordingViewSet(ModelViewSet):
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        DjangoModelPermissions,
    )
    filter_fields = ()

    def get_queryset(self):
        return get_objects_for_user(
            self.request.user,
            'video.view_recording',
            klass=self.queryset.model
        )


class RecordingAssetViewSet(ModelViewSet):
    queryset = RecordingAsset.objects.all()
    serializer_class = RecordingAssetSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        DjangoModelPermissions,
    )
    filter_fields = (
        'recording',
        'mimetype',
    )

    def get_queryset(self):
        return get_objects_for_user(
            self.request.user,
            'video.view_recordingasset',
            klass=self.queryset.model
        )


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (
        DjangoModelPermissions,
    )
    filter_fields = ()

    def get_queryset(self):
        return get_objects_for_user(
            self.request.user,
            'video.view_event',
            klass=self.queryset.model
        )


class DASHPublishViewSet(ModelViewSet):
    queryset = DASHPublish.objects.all()
    serializer_class = DASHPublishSerializer
    permission_classes = (
        DjangoModelPermissions,
    )
    filter_fields = ()

    def get_queryset(self):
        return get_objects_for_user(
            self.request.user,
            'video.view_dash',
            klass=self.queryset.model
        )


class DASHAudioViewSet(ModelViewSet):
    queryset = DASHAudio.objects.all()
    serializer_class = DASHAudioSerializer
    permission_classes = (
        DjangoModelPermissions,
    )
    filter_fields = ()

    def get_queryset(self):
        return get_objects_for_user(
            self.request.user,
            'video.view_dash_audio',
            klass=self.queryset.model
        )


class DASHVideoViewSet(ModelViewSet):
    queryset = DASHVideo.objects.all()
    serializer_class = DASHVideoSerializer
    permission_classes = (
        DjangoModelPermissions,
    )
    filter_fields = ()

    def get_queryset(self):
        return get_objects_for_user(
            self.request.user,
            'video.view_dash_video',
            klass=self.queryset.model
        )


class EpiphanViewSet(ModelViewSet):
    queryset = Epiphan.objects.all()
    serializer_class = EpiphanSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        DjangoModelPermissions,
    )
    filter_fields = ()


class EpiphanChannelViewSet(ModelViewSet):
    queryset = EpiphanChannel.objects.all()
    serializer_class = EpiphanChannelSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        DjangoModelPermissions,
    )
    filter_fields = ()


class EpiphanSourceViewSet(ModelViewSet):
    queryset = EpiphanSource.objects.all()
    serializer_class = EpiphanSourceSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        DjangoModelPermissions,
    )
    filter_fields = ()