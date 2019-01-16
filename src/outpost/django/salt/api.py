from rest_framework import (
    permissions,
    viewsets,
)

from . import (
    models,
    serializers,
)
from ..api.permissions import ExtendedDjangoModelPermissions


class HostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Host.objects.all()
    serializer_class = serializers.HostSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        ExtendedDjangoModelPermissions,
    )
