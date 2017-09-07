from django.views.generic import TemplateView
from rest_framework import (
    permissions,
    viewsets,
)

from . import (
    models,
    serializers,
)


class HoldingView(TemplateView):
    template_name = 'attendance/holding.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.room:
            return context
        room = models.Room.objects.get(pk=self.request.room)


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


class StudentViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
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
        permissions.DjangoModelPermissions,
    )

    def create(self, request):
        terminal = Terminal.objects.get(
            pk=request.data.get('terminal'),
            online=True
        )
        card = Card.objects.get(
            serial=request.data.get('serial'),
            active=True
        )
        room = terminal.room
        # TODO: Get holding if available
        try:
            holding = Holding.objects.get(
                room=terminal.room,
                state='running'
            )
        except Holding.DoesNotExist:
            holding = None
        student = card.student
        entry, created = Entry.objects.get_or_create(
            student=student,
            holding=holding
        )
        if not created:
            entry.leave()
            entry.save()
            status = 'OUT'
        else:
            status = 'IN'
        return Response({
            'status': status,
            'name': student,
            'holding': holding
        })
