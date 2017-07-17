import json
import re
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissions,
)
from rest_framework.filters import DjangoFilterBackend
# from rest_framework_extensions.mixins import (
#     CacheResponseAndETAGMixin,
# )
# from rest_framework_extensions.cache.mixins import (
#     CacheResponseMixin,
# )

from outpost.base.mixins import GeoModelViewSet
from outpost.geo.models import Edge
from . import (
    models,
    serializers,
)


class BeaconViewSet(GeoModelViewSet):
    """
    """
    queryset = models.Beacon.objects.filter(active=True)
    serializer_class = serializers.BeaconSerializer
    permission_classes = (
        DjangoModelPermissions,
    )
    pagination_class = None
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_fields = (
        'level',
    )


class LocateView(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )
    pattern = re.compile(r"^name\[(?P<name>\w+)\]$")
    query = """
        SELECT
            ST_ClosestPoint(e.path, b.position) AS position,
            e.id AS edge
        FROM
            geo_edge e,
            positioning_beacon b
        WHERE
            b.name = %s AND
            (
                b.level_id = (
                    SELECT level_id FROM geo_node WHERE id = e.source_id
                )
                OR
                b.level_id = (
                    SELECT level_id FROM geo_node WHERE id = e.destination_id
                )
            )
        ORDER BY
            ST_Distance(ST_ClosestPoint(e.path, b.position), b.position)
        LIMIT 1
    """

    def list(self, request, format=None):
        names = dict()
        for k, v in request.GET.items():
            if not k.startswith('name'):
                continue
            match = self.pattern.search(k)
            if not match:
                continue
            try:
                names[match.groupdict().get('name')] = float(v)
            except ValueError:
                continue
        if not names:
            raise NotFound(detail='No incoming signal data')
        conditions = [
            Q(name__in=names.keys()),
            Q(active=True),
        ]
        if 'edge' in request.GET:
            try:
                e = Edge.objects.get(pk=request.GET.get('edge'))
                conditions.append(Q(level=e.source.level) | Q(level=e.destination.level))
            except Edge.DoesNotExist:
                pass
        beacons = models.Beacon.objects.filter(*conditions)
        if not beacons:
            raise NotFound(detail='No matching beacon found')
        beacon = max(beacons, key=lambda b: names.get(b.name))
        with connection.cursor() as cursor:
            cursor.execute(self.query, [str(beacon.name)])
            if cursor.rowcount != 1:
                raise NotFound(detail='No matching edge found')
            point, edge = cursor.fetchone()
            geometry = GEOSGeometry(point)

            return Response({
                'geometry': {
                    'type': 'Point',
                    'coordinates': list(geometry)
                },
                'properties': {
                    'edge': edge,
                    'level': beacon.level.pk,
                },
                'type': 'Feature',
            })
