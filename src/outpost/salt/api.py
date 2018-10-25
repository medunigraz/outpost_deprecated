from rest_framework import (
    permissions,
    viewsets,
)

from outpost.api.permissions import ExtendedDjangoModelPermissions

from . import (
    models,
    serializers,
)


class HostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Host.objects.all()
    serializer_class = serializers.HostSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        ExtendedDjangoModelPermissions,
    )
