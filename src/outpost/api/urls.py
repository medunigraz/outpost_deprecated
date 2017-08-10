from django.conf.urls import (
    include,
    url,
)
from rest_framework.routers import DefaultRouter

from . import views as api
from ..attendance import views as attendance
from ..campusonline import views as campusonline
from ..geo import views as geo
from ..positioning import views as positioning
from ..structure import views as structure
from ..typo3 import views as typo3

v1 = DefaultRouter()
v1.register(
    r'api/autocomplete',
    api.AutocompleteViewSet,
    base_name='autocomplete'
)
v1.register(
    r'positioning/locate',
    positioning.LocateView,
    base_name='positioning-locate'
)
v1.register(
    r'positioning/beacons',
    positioning.BeaconViewSet
)
v1.register(
    r'geo/background',
    geo.BackgroundViewSet
)
v1.register(
    r'geo/level',
    geo.LevelViewSet
)
v1.register(
    r'geo/rooms',
    geo.RoomViewSet,
    base_name='geo-room-list'
)
v1.register(
    r'geo/roomcategory',
    geo.RoomCategoryViewSet,
    base_name='geo-roomcategory-list'
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
    r'geo/edgecategory',
    geo.EdgeCategoryViewSet
)
v1.register(
    r'geo/edges',
    geo.EdgeViewSet
)
v1.register(
    r'geo/pointofinterest',
    geo.PointOfInterestViewSet
)
v1.register(
    r'geo/pointofinterestinstance',
    geo.PointOfInterestInstanceViewSet
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
    r'structure/organization',
    structure.OrganizationViewSet,
)
v1.register(
    r'structure/person',
    structure.PersonViewSet,
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
