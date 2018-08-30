from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.filters import DjangoObjectPermissionsFilter
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.viewsets import ReadOnlyModelViewSet

from outpost.api.permissions import (
    ExtendedDjangoModelPermissions,
    ExtendedDjangoObjectPermissions,
)
from outpost.base.decorators import docstring_format

from . import (
    filters,
    models,
    serializers,
)

# from rest_framework_extensions.mixins import (
#     CacheResponseAndETAGMixin,
# )
# from rest_framework_extensions.cache.mixins import (
#     CacheResponseMixin,
# )


class RoomCategoryViewSet(ReadOnlyModelViewSet):
    queryset = models.RoomCategory.objects.all()
    serializer_class = serializers.RoomCategorySerializer
    permission_classes = (
        AllowAny,
    )


class RoomViewSet(ReadOnlyModelViewSet):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = (
        AllowAny,
    )
    filter_fields = (
        'category',
    )


class FloorViewSet(ReadOnlyModelViewSet):
    queryset = models.Floor.objects.all()
    serializer_class = serializers.FloorSerializer
    permission_classes = (
        AllowAny,
    )


class BuildingViewSet(ReadOnlyModelViewSet):
    queryset = models.Building.objects.all()
    serializer_class = serializers.BuildingSerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(filter=filters.FunctionFilter.__doc__)
class FunctionViewSet(ReadOnlyModelViewSet):
    '''
    List organizational functions from CAMPUSonline.

    {filter}
    '''
    queryset = models.Function.objects.all()
    serializer_class = serializers.FunctionSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_class = filters.FunctionFilter
    permission_classes = (
        IsAuthenticated,
    )


@docstring_format(filter=filters.OrganizationFilter.__doc__)
class OrganizationViewSet(ReadOnlyModelViewSet):
    '''
    List staff accounts from CAMPUSonline.

    {filter}
    '''
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_class = filters.OrganizationFilter
    permission_classes = (
        AllowAny,
    )


@docstring_format(filter=filters.PersonFilter.__doc__)
class PersonViewSet(ReadOnlyModelViewSet):
    '''
    List staff accounts from CAMPUSonline.

    {filter}
    '''
    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_class = filters.PersonFilter
    permission_classes = (
        AllowAny,
    )


class PersonOrganizationFunctionViewSet(ReadOnlyModelViewSet):
    queryset = models.PersonOrganizationFunction.objects.all()
    serializer_class = serializers.PersonOrganizationFunctionSerializer
    permission_classes = (
        IsAuthenticated,
    )


class EventViewSet(ReadOnlyModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    permission_classes = (
        AllowAny,
    )

    def get_queryset(self):
        return self.queryset.filter(show_end__gte=timezone.now())


class CourseGroupTermViewSet(ReadOnlyModelViewSet):
    queryset = models.CourseGroupTerm.objects.all()
    serializer_class = serializers.CourseGroupTermSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_class = filters.CourseGroupTermFilter
    permission_classes = (
        ExtendedDjangoModelPermissions,
    )


class BulletinViewSet(ReadOnlyModelViewSet):
    queryset = models.Bulletin.objects.all()
    serializer_class = serializers.BulletinSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_class = filters.BulletinFilter
