import re
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

    def list(self, request, format=None):
        #with connection.cursor() as cursor:
        #    cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        #    cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
        #    row = cursor.fetchone()
        macs = {self.pattern.search(m).groupdict().get('mac'): float(v) for m, v in request.GET.items() if m.startswith('mac')}
        return Response(macs)

