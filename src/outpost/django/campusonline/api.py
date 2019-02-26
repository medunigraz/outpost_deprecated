from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_haystack.viewsets import HaystackViewSet
from rest_flex_fields.views import FlexFieldsMixin
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from . import (
    filters,
    key_constructors,
    models,
    serializers,
)
from ..api.permissions import ExtendedDjangoModelPermissions
from ..base.decorators import docstring_format

# from rest_framework_extensions.mixins import (
#     CacheResponseAndETAGMixin,
# )
# from rest_framework_extensions.cache.mixins import (
#     CacheResponseMixin,
# )


class RoomCategoryViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    queryset = models.RoomCategory.objects.all()
    serializer_class = serializers.RoomCategorySerializer
    object_cache_key_func = key_constructors.PersonKeyConstructor()
    list_cache_key_func = key_constructors.PersonKeyConstructor()
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


@docstring_format(
    model=models.Function.__doc__,
    filter=filters.FunctionFilter.__doc__,
    serializer=serializers.FunctionSerializer.__doc__
)
class FunctionViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List organizational functions from CAMPUSonline.

    {model}
    {filter}
    {serializer}
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
    permit_list_expands = (
        'persons',
    )


@docstring_format(
    model=models.Organization.__doc__,
    filter=filters.OrganizationFilter.__doc__,
    serializer=serializers.OrganizationSerializer.__doc__
)
class OrganizationViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List organizations from CAMPUSonline.

    {model}
    {filter}
    {serializer}
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
    permit_list_expands = (
        'persons',
    )


@docstring_format(
    model=models.Person.__doc__,
    filter=filters.PersonFilter.__doc__,
    serializer=serializers.PersonSerializer.__doc__
)
class PersonViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List staff accounts from CAMPUSonline.

    {model}
    {filter}
    {serializer}
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
    permit_list_expands = (
        'functions',
        'organizations',
        'classification',
        'expertise',
        'knowledge',
        'education',
    )

    def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated():
            return serializers.AuthenticatedPersonSerializer
        else:
            return self.serializer_class


@docstring_format(filter=filters.PersonOrganizationFunctionFilter.__doc__)
class PersonOrganizationFunctionViewSet(ReadOnlyModelViewSet):
    '''
    Map person to organizational unit and function through CAMPUSonline.

    {filter}
    '''
    queryset = models.PersonOrganizationFunction.objects.all()
    serializer_class = serializers.PersonOrganizationFunctionSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_class = filters.PersonOrganizationFunctionFilter
    permission_classes = (
        IsAuthenticated,
    )


@docstring_format(
    model=models.DistributionList.__doc__,
    filter=filters.DistributionListFilter.__doc__,
    serializer=serializers.DistributionListSerializer.__doc__
)
class DistributionListViewSet(CacheResponseMixin, FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List distribution lists from CAMPUSonline.

    {model}
    {filter}
    {serializer}
    '''
    queryset = models.DistributionList.objects.all()
    serializer_class = serializers.DistributionListSerializer
    object_cache_key_func = key_constructors.DistributionListKeyConstructor()
    list_cache_key_func = key_constructors.DistributionListKeyConstructor()
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_class = filters.DistributionListFilter
    permission_classes = (
        IsAuthenticated,
    )
    permit_list_expands = (
        'persons',
    )


@docstring_format(
    model=models.Event.__doc__,
    filter=filters.EventFilter.__doc__
)
class EventViewSet(ReadOnlyModelViewSet):
    '''
    List events from CAMPUSonline.

    {model}
    {filter}
    '''
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_class = filters.EventFilter
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


@docstring_format(
    model=models.Bulletin.__doc__,
    filter=filters.BulletinFilter.__doc__
)
class BulletinViewSet(ReadOnlyModelViewSet):
    '''
    List official bulletins from CAMPUSonline.

    {model}
    {filter}
    '''
    queryset = models.Bulletin.objects.all()
    serializer_class = serializers.BulletinSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_class = filters.BulletinFilter


@docstring_format(
    model=models.BulletinPage.__doc__,
    filter=filters.BulletinPageFilter.__doc__
)
class BulletinPageViewSet(ReadOnlyModelViewSet):
    '''
    List official bulletin pages with extracted text from CAMPUSonline.

    {model}
    {filter}
    '''
    queryset = models.BulletinPage.objects.all()
    serializer_class = serializers.BulletinPageSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_class = filters.BulletinPageFilter
    permission_classes = (
        AllowAny,
    )


class BulletinPageSearchViewSet(HaystackViewSet):
    index_models = [models.BulletinPage]
    serializer_class = serializers.BulletinPageSearchSerializer
    permission_classes = (
        AllowAny,
    )
