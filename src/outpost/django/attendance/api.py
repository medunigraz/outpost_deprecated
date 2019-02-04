import logging

from django.db.models import Q
from django.shortcuts import get_object_or_404
from guardian.shortcuts import get_objects_for_user
from rest_framework import (
    exceptions,
    permissions,
    viewsets,
)
from rest_framework.filters import DjangoObjectPermissionsFilter
from rest_framework.response import Response

from ..api.permissions import ExtendedDjangoModelPermissions
from ..campusonline import models as co

from . import (
    models,
    serializers,
)

logger = logging.getLogger(__name__)


class TerminalViewSet(viewsets.ModelViewSet):
    queryset = models.Terminal.objects.all()
    serializer_class = serializers.TerminalSerializer
    permission_classes = (
        ExtendedDjangoModelPermissions,
    )


class ClockViewSet(viewsets.ViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def create(self, request):
        term_id = request.data.get('terminal')
        logger.debug(f'Incoming request for terminal {term_id}')
        try:
            terminal = models.Terminal.objects.get(
                pk=request.data.get('terminal'),
                online=True,
                enabled=True
            )
        except models.Terminal.DoesNotExist:
            logger.warn(f'Unknown terminal {term_id}')
            raise exceptions.NotFound('Unknown terminal identification')
        cardid = request.data.get('cardid', None)
        if not cardid:
            logger.warn(f'Missing card id')
            raise exceptions.ValidationError('Missing cardid information')
        try:
            student = co.Student.objects.get(cardid=cardid)
        except co.Student.DoesNotExist:
            logger.warn(f'No student found for cardid {cardid}')
            raise exceptions.NotFound('Unknown student identification')
        entry = models.Entry.objects.create(
            student=student,
            terminal=terminal
        )
        return Response({
            'status': entry.status,
            'name': str(student),
            'entry': entry.pk,
        })


class CampusOnlineHoldingViewSet(viewsets.ModelViewSet):
    queryset = models.CampusOnlineHolding.objects.all()
    serializer_class = serializers.CampusOnlineHoldingSerializer
    permission_classes = (
        ExtendedDjangoModelPermissions,
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
