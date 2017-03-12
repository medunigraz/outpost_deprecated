from django.conf.urls import (
    include,
    url,
)
from rest_framework.routers import DefaultRouter

from ..attendance import views as attendance
from ..geo import views as geo
from ..typo3 import views as typo3

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
v1.register(r'typo3/news', typo3.NewsViewSet)
v1.register(r'typo3/search/news', typo3.NewsSearchViewSet, base_name='news-search')
v1.register(r'typo3/categories', typo3.CategoryViewSet)

urlpatterns = [
    url(r'^v1/', include(v1.urls, namespace='v1')),
]
