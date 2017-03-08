from django.conf.urls import (
    include,
    url,
)
from rest_framework.routers import DefaultRouter

from ..attendance import views as attendance
from ..geo import views as geo

v1 = DefaultRouter()
v1.register(r'geo/rooms', geo.RoomViewSet)
v1.register(r'geo/doors', geo.DoorViewSet)
v1.register(r'geo/floors', geo.FloorViewSet)
v1.register(r'geo/buildings', geo.BuildingViewSet)
v1.register(r'geo/nodes', geo.NodeViewSet)
v1.register(r'geo/edges', geo.EdgeViewSet)
v1.register(r'geo/beacons', geo.BeaconViewSet)
v1.register(
    r'geo/routing/edges',
    geo.RoutingEdgeViewSet,
    base_name='edge-routing'
)
v1.register(
    r'geo/search/rooms',
    geo.RoomSearchViewSet,
    base_name='room-search'
)
v1.register(r'attendance/holdings', attendance.HoldingViewSet)
v1.register(r'attendance/entries', attendance.EntryViewSet)

urlpatterns = [
    url(r'^v1/', include(v1.urls, namespace='v1')),
]
