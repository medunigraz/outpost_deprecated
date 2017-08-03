from drf_haystack.viewsets import HaystackViewSet
from rest_framework.filters import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

# from rest_framework_extensions.mixins import (
#     CacheResponseAndETAGMixin,
# )
# from rest_framework_extensions.cache.mixins import (
#     CacheResponseMixin,
# )
from . import (
    models,
    serializers,
)


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
    filter_backends = (
        DjangoFilterBackend,
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


class OrganizationViewSet(ReadOnlyModelViewSet):
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
    permission_classes = (
        AllowAny,
    )


class PersonViewSet(ReadOnlyModelViewSet):
    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer
    permission_classes = (
        AllowAny,
    )
