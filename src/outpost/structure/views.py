from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

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


class PersonViewSet(ModelViewSet):
    queryset = models.Person.objects.filter(hidden=False)
    serializer_class = serializers.PersonSerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
    )
