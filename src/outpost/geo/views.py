from drf_haystack.viewsets import HaystackViewSet
from rest_framework.filters import DjangoFilterBackend
from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
)
from rest_framework_gis.filters import InBBoxFilter
# from rest_framework_extensions.mixins import (
#     CacheResponseAndETAGMixin,
# )
# from rest_framework_extensions.cache.mixins import (
#     CacheResponseMixin,
# )
from reversion.views import RevisionMixin

from outpost.base.mixins import MediatypeNegotiationMixin

from . import (
    filters,
    models,
    serializers,
)
from .key_constructors import RoutingEdgeKeyConstructor


class GeoModelViewSet(MediatypeNegotiationMixin, RevisionMixin, ModelViewSet):
    pass


class RoomViewSet(GeoModelViewSet):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    bbox_filter_field = 'layout'
    filter_backends = (
        DjangoFilterBackend,
        InBBoxFilter,
    )
    filter_fields = (
        'floor',
    )
    bbox_filter_include_overlapping = True


class RoomSearchViewSet(HaystackViewSet):
    index_models = [models.Room]
    serializer_class = serializers.RoomSearchSerializer


class DoorViewSet(GeoModelViewSet):
    queryset = models.Door.objects.all()
    serializer_class = serializers.DoorSerializer
    bbox_filter_field = 'line'
    filter_backends = (
        InBBoxFilter,
    )
    bbox_filter_include_overlapping = True


class FloorViewSet(RevisionMixin, ModelViewSet):
    queryset = models.Floor.objects.all()
    serializer_class = serializers.FloorSerializer
    filter_backends = (
        DjangoFilterBackend,
    )


class BuildingViewSet(GeoModelViewSet):
    queryset = models.Building.objects.all()
    serializer_class = serializers.BuildingSerializer
    bbox_filter_field = 'outline'
    filter_backends = (
        InBBoxFilter,
    )
    bbox_filter_include_overlapping = True


class NodeViewSet(GeoModelViewSet):
    queryset = models.Node.objects.all()
    serializer_class = serializers.NodeSerializer
    pagination_class = None
    bbox_filter_field = 'center'
    filter_backends = (
        DjangoFilterBackend,
        InBBoxFilter,
    )
    filter_fields = (
        'floor',
    )
    bbox_filter_include_overlapping = True


class EdgeViewSet(GeoModelViewSet):
    """
    Get edges from the navigation mesh.

    There are two options to filter edges by floors:

    First you can get all edges whose `source` or `destination` nodes are on a
    specific floor:

        ...?floor=<id>

    The other way is to filter specifically by the floor either the `source` or
    the `destination` node is on:

        ...?source__floor=<id>
        ...?destination__floor=<id>
    """
    queryset = models.Edge.objects.all()
    serializer_class = serializers.EdgeSerializer
    pagination_class = None
    bbox_filter_field = 'path'
    filter_backends = (
        DjangoFilterBackend,
        InBBoxFilter,
    )
    filter_class = filters.EdgeFilter
    bbox_filter_include_overlapping = True


class BeaconViewSet(GeoModelViewSet):
    """
    """
    queryset = models.Beacon.objects.filter(active=True)
    serializer_class = serializers.BeaconSerializer


class RoutingEdgeViewSet(MediatypeNegotiationMixin, ReadOnlyModelViewSet):
    """
    Query the edge graph for a route between two nodes:

        ...?from=<id>&to=<id>

    To limit the path to accessible routes only, add a key to the query:

        ...?from=<id>&to=<id>&accessible

    The order of the result resembles the sequence of paths required to take to
    get from **source** to **target**.
    """
    serializer_class = serializers.RoutingEdgeSerializer
    bbox_filter_field = 'path'
    pagination_class = None
    list_cache_key_func = RoutingEdgeKeyConstructor()

    statement = ("""
        SELECT
            r.seq AS sequence,
            e.*
        FROM
            geo_edge e,
            pgr_aStar('
                SELECT
                    e.id AS id,
                    ns.id AS source,
                    nd.id AS target,
                    ST_LENGTH(e.path) * e.weight AS cost,
                    CASE
                        e.one_way
                    WHEN
                        TRUE
                    THEN
                        -1
                    ELSE
                        ST_LENGTH(e.path) * e.weight
                    END AS reverse_cost,
                    ST_X(ns.center) AS x1,
                    ST_Y(ns.center) AS y1,
                    ST_X(nd.center) AS x2,
                    ST_Y(ns.center) AS y2
                FROM
                    geo_edge e,
                    geo_node nd,
                    geo_node ns
                WHERE
                    e.destination_id = nd.id AND
                    e.source_id = ns.id AND
                    CASE
                        e.accessible
                    WHEN
                        {accessible}
                    THEN
                        TRUE
                    ELSE
                        FALSE
                    END
            ', %(source)s, %(target)s) r
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
