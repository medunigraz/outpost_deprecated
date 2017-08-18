from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseNotFound,
    JsonResponse,
)
from django.shortcuts import get_object_or_404
from django.views.generic import View, TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Stream, Token, Broadcast, Recording, Export
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
        exporters = {c._meta.verbose_name: c.__name__ for c in classes}
        context['exporters'] = exporters
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
