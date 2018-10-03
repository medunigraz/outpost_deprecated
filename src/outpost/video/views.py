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

from .models import (
    Broadcast,
    DASHAudio,
    DASHPublish,
    DASHVideo,
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


class PublishRTMPView(NginxRTMPBackend):

    def handle(self, request, stream):
        stream.active = Broadcast.objects.create(stream=stream)
        stream.save()
        return HttpResponse()


class PublishDoneRTMPView(NginxRTMPBackend):

    def handle(self, request, stream):
        stream.active.end = timezone.now()
        stream.active.save()
        stream.active = None
        stream.save()
        return HttpResponse()


class DASHView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Event
    permission_required = 'video.add_publish'
    template_name_suffix = '_publish_dash'


class DASHMediaView(PathDownloadView):
    model = None

    def get_path(self):
        media = get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        path = Path(media.path).joinpath(super().get_path())
        if not path.is_absolute():
            return HttpResponseNotFound()
        if not path.is_file():
            return HttpResponseNotFound()
        return str(path)
