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

from outpost.api.permissions import ExtendedDjangoModelPermissions
from outpost.campusonline import models as co

from . import (
    models,
    serializers,
)


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
