from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseNotFound,
    JsonResponse,
)
from django.shortcuts import get_object_or_404
from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
    View,
)
from rest_framework.viewsets import (
    ModelViewSet,
)
from rest_framework.filters import DjangoFilterBackend
from rest_framework.permissions import (
    AllowAny,
    DjangoModelPermissions,
    DjangoModelPermissionsOrAnonReadOnly,
    IsAuthenticatedOrReadOnly,
)
from guardian.shortcuts import get_objects_for_user

from .models import (
    Broadcast,
    Export,
    Recorder,
    Recording,
    RecordingAsset,
    Epiphan,
    EpiphanChannel,
    Stream,
    Token,
)
from .serializers import (
    RecorderSerializer,
    RecordingSerializer,
    RecordingAssetSerializer,
)
from .tasks import ExportTask


class NginxRTMPBackend(View):

    def post(self, request):
        value = request.POST.get('name')
        key = request.GET.get('token', None)
        if not key:
            return HttpResponseForbidden()
        stream = get_object_or_404(Stream, pk=value)
        if not stream.enabled:
            return HttpResponseForbidden()
        get_object_or_404(Token, value=key, stream=stream)
        return self.handle(request, stream)


class PublishView(NginxRTMPBackend):

    def handle(self, request, stream):
        stream.active = Broadcast.objects.create(stream=stream)
        stream.save()
        return HttpResponse()


class PublishDoneView(NginxRTMPBackend):

    def handle(self, request, stream):
        stream.active.end = timezone.now()
        stream.active.save()
        stream.active = None
        stream.save()
        return HttpResponse()


class RecordingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Recording
    permission_required = 'video.change_recording'


class RecordingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Recording
    permission_required = 'video.change_recording'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classes = Export.__subclasses__()
        exporters = [(c._meta.verbose_name, c.__name__) for c in classes]
        context['exporters'] = sorted(exporters, key=lambda x: x[1])
        return context


class RecordingExportView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'video.change_recording'

    def post(self, request, pk, exporter):
        task = ExportTask.delay(pk, exporter)
        return JsonResponse(
            {
                'task': task.id,
            }
        )


class RecorderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Recorder
    permission_required = 'video.change_recorder'


class RecorderDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Recorder
    permission_required = 'video.change_recorder'


class EpiphanChannelView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'video.change_recorder'
    http_method_names = [
        'get',
        'start',
        'stop',
    ]

    def get(self, request, pk, channel):
        epiphan = get_object_or_404(Epiphan, pk=pk)
        obj = get_object_or_404(EpiphanChannel, pk=channel, epiphan=epiphan)
        return JsonResponse(obj.response())

    def start(self, request, pk, channel):
        epiphan = get_object_or_404(Epiphan, pk=pk)
        obj = get_object_or_404(EpiphanChannel, pk=channel, epiphan=epiphan)
        obj.start()
        return JsonResponse(obj.response())

    def stop(self, request, pk, channel):
        epiphan = get_object_or_404(Epiphan, pk=pk)
        obj = get_object_or_404(EpiphanChannel, pk=channel, epiphan=epiphan)
        obj.stop()
        return JsonResponse(obj.response())


class RecorderViewSet(ModelViewSet):
    queryset = Recorder.objects.all()
    serializer_class = RecorderSerializer
    permission_classes = (
        DjangoModelPermissions,
    )
    filter_backends = (
        DjangoFilterBackend,
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
    permission_classes = (
        DjangoModelPermissions,
    )
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_fields = ()

    def get_queryset(self):
        return get_objects_for_user(
            self.request.user,
            'video.view_recording',
            klass=self.queryset
        )


class RecordingAssetViewSet(ModelViewSet):
    queryset = RecordingAsset.objects.all()
    serializer_class = RecordingAssetSerializer
    permission_classes = (
        DjangoModelPermissions,
    )
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_fields = ()

    def get_queryset(self):
        return get_objects_for_user(
            self.request.user,
            'video.view_recordingasset',
            klass=self.queryset
        )
