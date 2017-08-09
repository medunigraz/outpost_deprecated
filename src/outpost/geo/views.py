import re

from braces.views import CsrfExemptMixin
from django.db import connection
from drf_haystack.viewsets import HaystackViewSet
from oauth2_provider.ext.rest_framework import IsAuthenticatedOrTokenHasScope
from rest_framework import viewsets
from rest_framework.filters import DjangoFilterBackend
from rest_framework.permissions import (
    AllowAny,
    DjangoModelPermissions,
    DjangoModelPermissionsOrAnonReadOnly,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
)
# from rest_framework_extensions.mixins import (
#     CacheResponseAndETAGMixin,
# )
# from rest_framework_extensions.cache.mixins import (
#     CacheResponseMixin,
# )
from rest_framework_extensions.cache.mixins import ListCacheResponseMixin
from rest_framework_extensions.etag.mixins import ListETAGMixin
from rest_framework_gis.filters import InBBoxFilter
from reversion.views import RevisionMixin

from outpost.base.mixins import (
    GeoModelViewSet,
    MediatypeNegotiationMixin,
)

from . import key_constructors as keys
from . import (
    filters,
    models,
    serializers,
)


class BackgroundViewSet(ListETAGMixin, ListCacheResponseMixin, GeoModelViewSet):
    queryset = models.Background.objects.all()
    serializer_class = serializers.BackgroundSerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
    )
    pagination_class = None
    bbox_filter_field = 'layout'
    filter_backends = (
        InBBoxFilter,
    )
    bbox_filter_include_overlapping = True
    list_cache_key_func = keys.BackgroundListKeyConstructor()
    list_etag_func = keys.BackgroundListKeyConstructor()


class LevelViewSet(ModelViewSet):
    queryset = models.Level.objects.all()
    serializer_class = serializers.LevelSerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
    )


class RoomCategoryViewSet(RevisionMixin, ModelViewSet):
    queryset = models.RoomCategory.objects.all()
    serializer_class = serializers.RoomCategorySerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
    )
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_fields = (
        'searchable',
    )


class RoomViewSet(ListETAGMixin, ListCacheResponseMixin, GeoModelViewSet):
    """
    Get rooms with geographic layout and metadata.

    Several filters are supported:

        ?level=<id>
        ?campusonline=<id>
        ?category=<id>

    Filters can be combined:

        ?level=<id>&category=<id>
    """
    queryset = models.Room.objects.filter(deprecated=False)
    serializer_class = serializers.RoomSerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
    )
    pagination_class = None
    bbox_filter_field = 'layout'
    filter_backends = (
        DjangoFilterBackend,
        InBBoxFilter,
    )
    filter_class = filters.RoomFilter
    bbox_filter_include_overlapping = True
    list_cache_key_func = keys.RoomListKeyConstructor()
    list_etag_func = keys.RoomListKeyConstructor()


class RoomSearchViewSet(HaystackViewSet):
    index_models = [models.Room]
    serializer_class = serializers.RoomSearchSerializer
    permission_classes = (
        AllowAny,
    )


class DoorViewSet(ListETAGMixin, ListCacheResponseMixin, GeoModelViewSet):
    queryset = models.Door.objects.filter(deprecated=False)
    serializer_class = serializers.DoorSerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
    )
    pagination_class = None
    filter_backends = (
        DjangoFilterBackend,
        InBBoxFilter,
    )
    filter_class = filters.DoorFilter
    bbox_filter_field = 'layout'
    bbox_filter_include_overlapping = True
    list_cache_key_func = keys.DoorListKeyConstructor()
    list_etag_func = keys.DoorListKeyConstructor()


class FloorViewSet(ListETAGMixin, ListCacheResponseMixin, RevisionMixin, ModelViewSet):
    queryset = models.Floor.objects.all()
    serializer_class = serializers.FloorSerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
    )
    pagination_class = None
    filter_backends = (
        DjangoFilterBackend,
        InBBoxFilter,
    )
    filter_class = filters.FloorFilter
    bbox_filter_field = 'outline'
    bbox_filter_include_overlapping = True
    list_cache_key_func = keys.FloorListKeyConstructor()
    list_etag_func = keys.FloorListKeyConstructor()


class BuildingViewSet(ListETAGMixin, ListCacheResponseMixin, GeoModelViewSet):
    queryset = models.Building.objects.all()
    serializer_class = serializers.BuildingSerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
    )
    pagination_class = None
    filter_backends = (
        DjangoFilterBackend,
        InBBoxFilter,
    )
    filter_class = filters.BuildingFilter
    bbox_filter_field = 'outline'
    bbox_filter_include_overlapping = True
    list_cache_key_func = keys.BuildingListKeyConstructor()
    list_etag_func = keys.BuildingListKeyConstructor()


class NodeViewSet(ListETAGMixin, ListCacheResponseMixin, GeoModelViewSet):
    queryset = models.Node.objects.all()
    serializer_class = serializers.NodeSerializer
    permission_classes = (
        IsAuthenticatedOrTokenHasScope,
        DjangoModelPermissions,
    )
    pagination_class = None
    filter_backends = (
        DjangoFilterBackend,
        InBBoxFilter,
    )
    filter_class = filters.NodeFilter
    bbox_filter_field = 'center'
    bbox_filter_include_overlapping = True
    list_cache_key_func = keys.NodeListKeyConstructor()
    list_etag_func = keys.NodeListKeyConstructor()
    required_scopes = (
        'editor',
    )


class EdgeCategoryViewSet(ModelViewSet):
    """
    """
    queryset = models.EdgeCategory.objects.all()
    serializer_class = serializers.EdgeCategorySerializer
    permission_classes = (
        IsAuthenticatedOrTokenHasScope,
        DjangoModelPermissions,
    )
    pagination_class = None
    required_scopes = (
        'editor',
    )


class EdgeViewSet(ListETAGMixin, ListCacheResponseMixin, GeoModelViewSet):
    """
    Get edges from the navigation mesh.

    There are two options to filter edges by level:

    First you can get all edges whose `source` or `destination` nodes are on a
    specific level:

        ...?level=<id>

    The other way is to filter specifically by the level either the `source` or
    the `destination` node is on:

        ...?source__level=<id>
        ...?destination__level=<id>
    """
    queryset = models.Edge.objects.all()
    serializer_class = serializers.EdgeSerializer
    permission_classes = (
        IsAuthenticatedOrTokenHasScope,
        DjangoModelPermissions,
    )
    required_scopes = (
        'editor',
    )
    pagination_class = None
    filter_backends = (
        DjangoFilterBackend,
        InBBoxFilter,
    )
    filter_class = filters.EdgeFilter
    bbox_filter_field = 'path'
    bbox_filter_include_overlapping = True
    list_cache_key_func = keys.EdgeListKeyConstructor()
    list_etag_func = keys.EdgeListKeyConstructor()


class PointOfInterestViewSet(ListETAGMixin, ListCacheResponseMixin, ModelViewSet):
    """
    """
    queryset = models.PointOfInterest.objects.all()
    serializer_class = serializers.PointOfInterestSerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
    )
    pagination_class = None
    list_cache_key_func = keys.PointOfInterestListKeyConstructor()
    list_etag_func = keys.PointOfInterestListKeyConstructor()


class PointOfInterestInstanceViewSet(ListETAGMixin, ListCacheResponseMixin, GeoModelViewSet):
    """
    """
    queryset = models.PointOfInterestInstance.objects.all()
    serializer_class = serializers.PointOfInterestInstanceSerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
    )
    pagination_class = None
    filter_backends = (
        DjangoFilterBackend,
        InBBoxFilter,
    )
    filter_class = filters.PointOfInterestInstanceFilter
    bbox_filter_field = 'center'
    bbox_filter_include_overlapping = True
    list_cache_key_func = keys.PointOfInterestInstanceListKeyConstructor()
    list_etag_func = keys.PointOfInterestInstanceListKeyConstructor()


class RoutingEdgeViewSet(ListETAGMixin, ListCacheResponseMixin, MediatypeNegotiationMixin, ReadOnlyModelViewSet):
    """
    Query the edge graph for a route between two nodes:

        ...?from=<id>&to=<id>

    To limit the path to accessible routes only, add a key to the query:

        ...?from=<id>&to=<id>&accessible

    The order of the result resembles the sequence of paths required to take to
    get from **source** to **target**.
    """
    serializer_class = serializers.RoutingEdgeSerializer
    permission_classes = (
        AllowAny,
    )
    bbox_filter_field = 'path'
    pagination_class = None
    list_cache_key_func = keys.RoutingEdgeListKeyConstructor()
    list_etag_func = keys.RoutingEdgeListKeyConstructor()

    statement = ("""
        SELECT
            r.seq AS sequence,
            e.*
        FROM
            geo_edge e,
            pgr_aStar(
                '
                SELECT
                    e.id AS id,
                    ns.id AS source,
                    nd.id AS target,
                    (ST_LENGTH(e.path) + c.addition) * c.multiplicator AS cost,
                    CASE
                        e.one_way
                    WHEN
                        TRUE
                    THEN
                        -1
                    ELSE
                        (ST_LENGTH(e.path) + c.addition) * c.multiplicator
                    END AS reverse_cost,
                    ST_X(ns.center) AS x1,
                    ST_Y(ns.center) AS y1,
                    ST_X(nd.center) AS x2,
                    ST_Y(ns.center) AS y2
                FROM
                    geo_edge e,
                    geo_edgecategory c,
                    geo_node nd,
                    geo_node ns
                WHERE
                    e.destination_id = nd.id AND
                    e.source_id = ns.id AND
                    e.category_id = c.id AND
                    CASE
                        e.accessible
                    WHEN
                        {accessible}
                    THEN
                        TRUE
                    ELSE
                        FALSE
                    END
                '::text,
                %(source)s::integer,
                %(target)s::integer,
                directed := false,
                heuristic := 3
            ) r
        WHERE
            r.edge = e.id AND
            r.edge >= 0
        ORDER BY r.seq ASC""")

    def get_queryset(self):
        source = self.request.GET.get('from', None)
        target = self.request.GET.get('to', None)
        accessible = 'accessible' in self.request.GET
        if not all((source, target)):
            return models.Edge.objects.none()
        return models.Edge.objects.raw(
            self.statement.format(
                accessible=str(accessible).upper()
            ),
            dict(
                source=source,
                target=target
            )
        )
