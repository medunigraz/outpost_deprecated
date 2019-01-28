import re

from django.contrib.gis.geos import GEOSGeometry
from django.core.cache import cache
from django.db.models import Q
from oauth2_provider.contrib.rest_framework import IsAuthenticatedOrTokenHasScope
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    DjangoModelPermissions,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from . import (
    models,
    serializers,
)
from ..base.mixins import GeoModelViewSet
from ..geo.models import Edge

# from rest_framework_extensions.mixins import (
#     CacheResponseAndETAGMixin,
# )
# from rest_framework_extensions.cache.mixins import (
#     CacheResponseMixin,
# )


class BeaconViewSet(GeoModelViewSet):
    """
    """
    queryset = models.Beacon.objects.filter(active=True)
    serializer_class = serializers.BeaconSerializer
    permission_classes = (
        IsAuthenticatedOrTokenHasScope,
        DjangoModelPermissions,
    )
    required_scopes = (
        'editor',
    )
    pagination_class = None
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
            e.id AS edge,
            e.path AS path,
            CASE WHEN
                ST_Distance(b.position, nd.center) < ST_Distance(b.position, ns.center)
            THEN
                nd.id
            ELSE
                ns.id
            END AS node
        FROM
            geo_edge e,
            geo_node ns,
            geo_node nd,
            positioning_beacon b
        WHERE
            b.name = %s AND
            e.source_id = ns.id AND
            e.destination_id = nd.id AND
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
        LIMIT 1"""

    def list(self, request, format=None):
        from django.db import connection
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
                conditions.append(
                    Q(level=e.source.level) | Q(level=e.destination.level)
                )
            except Edge.DoesNotExist:
                pass
        beacons = models.Beacon.objects.filter(*conditions)
        if not beacons:
            raise NotFound(detail='No matching beacon found')
        beacon = max(beacons, key=lambda b: names.get(b.name))
        key = 'positioning-locate-beacon-{}'.format(beacon.pk)
        data = cache.get(key)
        if not data:
            with connection.cursor() as cursor:
                cursor.execute(self.query, [str(beacon.name)])
                if cursor.rowcount != 1:
                    raise NotFound(detail='No matching edge found')
                point, edge, path, node = cursor.fetchone()

                data = {
                    'geometry': {
                        'type': 'Point',
                        'coordinates': list(GEOSGeometry(point))
                    },
                    'properties': {
                        'edge': edge,
                        'path': {
                            'type': 'Feature',
                            'geometry': {
                                'coordinates': list(GEOSGeometry(path)),
                                'type': 'LineString'
                            }
                        },
                        'node': node,
                        'level': beacon.level.pk,
                    },
                    'type': 'Feature',
                }
                cache.set(key, data, timeout=600)
        connection.close()
        return Response(data)
