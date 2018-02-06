from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.viewsets import ModelViewSet

from . import (
    models,
    serializers,
)


class OrganizationViewSet(ModelViewSet):
    queryset = models.Organization.objects.filter(hidden=False)
    serializer_class = serializers.OrganizationSerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
    )
    pagination_class = None
    filter_fields = (
        'color',
        'campusonline',
        'office',
    )


class PersonViewSet(ModelViewSet):
    queryset = models.Person.objects.filter(hidden=False)
    serializer_class = serializers.PersonSerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
    )
    filter_fields = (
        'room',
    )
