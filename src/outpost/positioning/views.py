import json
import re
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
# from rest_framework_extensions.mixins import (
#     CacheResponseAndETAGMixin,
# )
# from rest_framework_extensions.cache.mixins import (
#     CacheResponseMixin,
# )

from outpost.base.mixins import GeoModelViewSet
from . import (
    models,
    serializers,
)


class BeaconViewSet(GeoModelViewSet):
    """
    """
    queryset = models.Beacon.objects.filter(active=True)
    serializer_class = serializers.BeaconSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]


class LocateView(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = [
        AllowAny,
    ]
    pattern = re.compile(r"^mac\[(?P<mac>(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2}))\]$")
    query = """
        SELECT
            ST_ClosestPoint(e.path, b.position) AS position,
            e.id AS edge
        FROM
            geo_edge e,
            positioning_beacon b
        WHERE
            b.mac = %s AND
            (
                b.level_id = (
                    SELECT level_id FROM geo_node WHERE id = e.source_id
                )
                OR
                b.level_id = (
                    SELECT level_id FROM geo_node WHERE id = e.source_id
                )
            )
        ORDER BY
            ST_Distance(ST_ClosestPoint(e.path, b.position), b.position)
        LIMIT 1
    """

    def list(self, request, format=None):
        macs = {self.pattern.search(m).groupdict().get('mac'): float(v) for m, v in request.GET.items() if m.startswith('mac')}
        if not macs:
            return Response()
        mac = max(macs, key=macs.get)
        with connection.cursor() as cursor:
            cursor.execute(self.query, [mac])
            point, edge = cursor.fetchone()
            geometry = GEOSGeometry(point)


            return Response({
                'geometry': {
                    'type': 'Point',
                    'coordinates': list(geometry)
                },
                'properties': {
                    'edge': edge,
                },
                'type': 'Feature',
            })
