from django.conf.urls import (
    include,
    url,
)
from rest_framework.routers import DefaultRouter

from ..attendance import views as attendance
from ..geo import views as geo
from ..typo3 import views as typo3
from ..campusonline import views as campusonline

v1 = DefaultRouter()
v1.register(
    r'geo/rooms',
    geo.RoomViewSet,
    base_name='geo-room-list'
)
v1.register(
    r'geo/doors',
    geo.DoorViewSet
)
v1.register(
    r'geo/floors',
    geo.FloorViewSet,
    base_name='geo-floor-list'
)
v1.register(
    r'geo/buildings',
    geo.BuildingViewSet,
    base_name='geo-building-list'
)
v1.register(
    r'geo/nodes',
    geo.NodeViewSet
)
v1.register(
    r'geo/edges',
    geo.EdgeViewSet
)
v1.register(
    r'geo/beacons',
    geo.BeaconViewSet
)
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
v1.register(
    r'geo/autocomplete',
    geo.AutocompleteViewSet,
    base_name='autocomplete'
)
v1.register(
    r'attendance/holdings',
    attendance.HoldingViewSet
)
v1.register(
    r'attendance/entries',
    attendance.EntryViewSet
)
v1.register(
    r'campusonline/room',
    campusonline.RoomViewSet,
    base_name='campusonline-room-list'
)
v1.register(
    r'campusonline/floor',
    campusonline.FloorViewSet,
    base_name='campusonline-floor-list'
)
v1.register(
    r'campusonline/building',
    campusonline.BuildingViewSet,
    base_name='campusonline-building-list'
)
v1.register(
    r'typo3/languages',
    typo3.LanguageViewSet
)
v1.register(
    r'typo3/categories',
    typo3.CategoryViewSet
)
v1.register(
    r'typo3/calendars',
    typo3.CalendarViewSet
)
v1.register(
    r'typo3/events',
    typo3.EventViewSet
)
v1.register(
    r'typo3/search/events',
    typo3.EventSearchViewSet,
    base_name='event-search'
)
v1.register(
    r'typo3/news',
    typo3.NewsViewSet
)
v1.register(
    r'typo3/search/news',
    typo3.NewsSearchViewSet,
    base_name='news-search'
)

urlpatterns = [
    url(r'^v1/', include(v1.urls, namespace='v1')),
]
