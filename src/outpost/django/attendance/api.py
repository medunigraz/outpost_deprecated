import logging

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from guardian.shortcuts import get_objects_for_user
from rest_flex_fields.views import FlexFieldsMixin
from rest_framework import (
    exceptions,
    permissions,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.filters import (
    DjangoObjectPermissionsFilter,
    OrderingFilter,
)
from rest_framework.response import Response

from . import (
    filters,
    models,
    serializers,
)
from ..api.permissions import ExtendedDjangoModelPermissions
from ..campusonline import models as co

logger = logging.getLogger(__name__)


class TerminalViewSet(FlexFieldsMixin, viewsets.ModelViewSet):
    queryset = models.Terminal.objects.all()
    serializer_class = serializers.TerminalSerializer
    permission_classes = (
        ExtendedDjangoModelPermissions,
    )
    permit_list_expands = (
        'rooms',
    )


class ClockViewSet(viewsets.ViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def create(self, request):
        terminal_id = request.data.get('terminal')
        logger.debug(f'Incoming request for terminal {terminal_id}')
        try:
            terminal = models.Terminal.objects.get(
                pk=terminal_id,
                online=True,
                enabled=True
            )
        except models.Terminal.DoesNotExist:
            logger.warn(f'Unknown terminal {terminal_id}')
            raise exceptions.NotFound('Unknown terminal identification')
        room_id = request.data.get('room')
        try:
            room = terminal.rooms.get(
                pk=room_id
            )
        except terminal.rooms.DoesNotExist:
            logger.warn(f'Unknown room {room_id}')
            raise exceptions.NotFound('Unknown room identification')
        card_id = request.data.get('cardid', None)
        if not card_id:
            logger.warn(f'Missing card id')
            raise exceptions.ValidationError('Missing card information')
        try:
            student = co.Student.objects.get(cardid=card_id)
        except co.Student.DoesNotExist:
            logger.warn(f'No student found for cardid {card_id}')
            raise exceptions.NotFound('Unknown student identification')
        entry = models.Entry.objects.create(
            student=student,
            terminal=terminal,
            room=room
        )
        return Response({
            'status': entry.status,
            'name': str(student),
            'entry': entry.pk,
            'room': room
        })


class CampusOnlineHoldingViewSet(FlexFieldsMixin, viewsets.ModelViewSet):
    queryset = models.CampusOnlineHolding.objects.all()
    serializer_class = serializers.CampusOnlineHoldingSerializer
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filter_class = filters.CampusOnlineHoldingFilter
    ordering_fields = (
        'initiated',
        'finished',
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )
    permit_list_expands = (
        'entries',
    )

    def get_queryset(self):
        username = self.request.user.username
        return self.queryset.filter(
            lecturer__username=username
        )


class CampusOnlineEntryViewSet(FlexFieldsMixin, viewsets.ModelViewSet):
    queryset = models.CampusOnlineEntry.objects.all()
    serializer_class = serializers.CampusOnlineEntrySerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    permit_list_expands = (
        'holding',
        'student',
    )

    def get_queryset(self):
        username = self.request.user.username
        return self.queryset.filter(
            holding__lecturer__username=username
        )


class StatisticsViewSet(viewsets.ModelViewSet):
    queryset = models.Statistics.objects.all()
    serializer_class = serializers.StatisticsSerializer
    permission_classes = (
        ExtendedDjangoModelPermissions,
    )
    filter_backends = (
        DjangoObjectPermissionsFilter,
    )

    #def get_queryset(self):
    #    return get_objects_for_user(
    #        self.request.user,
    #        'attendance.view_statistics',
    #        klass=self.queryset.model
    #    )
