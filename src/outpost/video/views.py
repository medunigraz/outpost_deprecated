import json
from pathlib import Path

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.http import (
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
from rest_framework.filters import DjangoFilterBackend
from rest_framework.permissions import (
    AllowAny,
    DjangoModelPermissions,
    DjangoModelPermissionsOrAnonReadOnly,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.viewsets import ModelViewSet

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
    Recorder,
    Recording,
    RecordingAsset,
    Stream,
    Token,
)
from .serializers import (
    EventSerializer,
    RecorderSerializer,
    EpiphanSerializer,
    EpiphanChannelSerializer,
    EpiphanSourceSerializer,
    RecordingAssetSerializer,
    RecordingSerializer,
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
    paginate_by = 10


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


class EventListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Event
    permission_required = 'video.add_event'


class EventCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Event
    permission_required = 'video.add_event'
    fields = (
        'title',
        'subject',
        'description',
        'license',
        'rights',
        'presenters',
        'contributors',
        'room',
    )

    def get_success_url(self):
        return reverse('video:event:list')


class EventUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    permission_required = 'video.change_event'


class EventDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Event
    permission_required = 'video.change_event'

    def delete(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.delete()
        return HttpResponse()


class EventMediaView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'video.change_event'
    mapping = {
        'video/mp4': EventVideo,
        'video/webm': EventVideo,
        'video/ogg': EventVideo,
        'audio/mp4': EventAudio,
        'audio/x-m4a': EventAudio,
        'audio/mpeg': EventAudio,
        'audio/webm': EventAudio,
        'audio/ogg': EventAudio,
        'audio/wav': EventAudio,
        'audio/wave': EventAudio,
        'audio/flac': EventAudio,
        'audio/aac': EventAudio,
    }

    def post(self, request, pk, media=None):
        event = get_object_or_404(Event, pk=pk)
        f = request.FILES.get('file')
        if f.content_type not in self.mapping:
            return HttpResponseBadRequest(
                'Unsupported mimetype: {}'.format(f.content_type)
            )
        obj = self.mapping.get(f.content_type)(event=event, name=f.name)
        obj.data.save(f.name, f)
        return JsonResponse(obj.response())

    def get(self, request, pk, media):
        event = get_object_or_404(Event, pk=pk)
        obj = get_object_or_404(EventMedia, pk=media)
        return JsonResponse(obj.response())

    def delete(self, request, pk, media):
        event = get_object_or_404(Event, pk=pk)
        obj = get_object_or_404(EventMedia, pk=media)
        obj.delete()
        return JsonResponse({})


class PublishView(LoginRequiredMixin, DetailView):
    model = Publish


class DASHView(PathDownloadView):

    model = None

    def get_path(self):
        media = get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        path = Path(media.path).joinpath(super().get_path())
        if not path.is_absolute():
            return HttpResponseNotFound()
        if not path.is_file():
            return HttpResponseNotFound()
        return str(path)


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
            klass=self.queryset.model
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
            klass=self.queryset.model
        )


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
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
            'video.view_event',
            klass=self.queryset
        )


class EpiphanViewSet(ModelViewSet):
    queryset = Epiphan.objects.all()
    serializer_class = EpiphanSerializer
    permission_classes = (
        DjangoModelPermissions,
    )
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_fields = ()


class EpiphanChannelViewSet(ModelViewSet):
    queryset = EpiphanChannel.objects.all()
    serializer_class = EpiphanChannelSerializer
    permission_classes = (
        DjangoModelPermissions,
    )
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_fields = ()


class EpiphanSourceViewSet(ModelViewSet):
    queryset = EpiphanSource.objects.all()
    serializer_class = EpiphanSourceSerializer
    permission_classes = (
        DjangoModelPermissions,
    )
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_fields = ()
