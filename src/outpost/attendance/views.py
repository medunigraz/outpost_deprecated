from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.views.generic import TemplateView
from rest_framework import (
    permissions,
    viewsets,
    exceptions,
)
from rest_framework.response import Response

from . import (
    models,
    serializers,
)
from ..campusonline import models as co


class HoldingView(TemplateView):
    template_name = 'attendance/holding.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = co.Room.objects.get(pk=self.kwargs['room'])
        return context


class TerminalViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = models.Terminal.objects.all()
    serializer_class = serializers.TerminalSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
    )


class HoldingViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = models.Holding.objects.all()
    serializer_class = serializers.HoldingSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
    )


class EntryViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = models.Entry.objects.all()
    serializer_class = serializers.EntrySerializer
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
    )


class ClockViewSet(viewsets.ViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def create(self, request):
        try:
            terminal = models.Terminal.objects.get(
                pk=request.data.get('terminal'),
                online=True,
                enabled=True
            )
        except models.Terminal.DoesNotExist:
            raise exceptions.NotFound('Unknown terminal identification')
        cardid = request.data.get('cardid', None)
        if not cardid:
            raise exceptions.ValidationError('Missing cardid information')
        student = None
        try:
            student = co.Student.objects.get(cardid=cardid)
        except co.Student.DoesNotExist:
            matriculation = request.data.get('matriculation', None)
            if matriculation:
                try:
                    student = co.Student.objects.get(matriculation=matriculation)
                except co.Student.DoesNotExist:
                    pass
        if not student:
            raise exceptions.NotFound('Unknown student identification')
        room = terminal.room
        # TODO: Get holding if available
        try:
            holding = models.Holding.objects.get(
                room=terminal.room,
                state='running'
            )
        except models.Holding.DoesNotExist:
            holding = None
        try:
            entry = models.Entry.objects.get(
                Q(student=student),
                Q(holding=holding),
                Q(room=terminal.room),
                Q(state='registered') | Q(state='assigned')
            )
            if entry.state == 'registered':
                entry.cancel()
            if entry.state == 'assigned':
                entry.leave()
            entry.save()
            status = 'OUT'
        except models.Entry.DoesNotExist:
            status = 'IN'
            entry = models.Entry.objects.create(
                student=student,
                holding=holding,
                room=terminal.room
            )
        return Response({
            'status': status,
            'name': str(student),
            'holding': holding and str(holding) or None,
            'entry': entry.pk,
        })
