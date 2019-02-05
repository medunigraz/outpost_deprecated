from django.conf.urls import (
    include,
    url,
)
from rest_framework.routers import DefaultRouter

from . import views as api
from ..attendance import api as attendance
from ..base import api as base
from ..campusonline import api as campusonline
from ..geo import api as geo
from ..networktoken import api as networktoken
from ..positioning import api as positioning
from ..research import api as research
from ..restaurant import api as restaurant
from ..salt import api as salt
from ..structure import api as structure
from ..thesis import api as thesis
from ..typo3 import api as typo3
from ..video import api as video

v1 = DefaultRouter()
v1.register(
    r'api/autocomplete',
    api.AutocompleteViewSet,
    base_name='api-autocomplete'
)
v1.register(
    r'base/contenttype',
    base.ContentTypeViewSet,
    base_name='base-contenttype'
)
v1.register(
    r'base/notification',
    base.NotificationViewSet,
    base_name='base-notification'
)
v1.register(
    r'base/task',
    base.TaskViewSet,
    base_name='base-task'
)
v1.register(
    r'base/password-strength',
    base.PasswordStrengthViewSet,
    base_name='base-password-strength'
)
v1.register(
    r'positioning/locate',
    positioning.LocateView,
    base_name='positioning-locate'
)
v1.register(
    r'positioning/beacons',
    positioning.BeaconViewSet,
    base_name='positioning-beacons'
)
v1.register(
    r'geo/background',
    geo.BackgroundViewSet,
    base_name='geo-background'
)
v1.register(
    r'geo/level',
    geo.LevelViewSet,
    base_name='geo-level'
)
v1.register(
    r'geo/rooms',
    geo.RoomViewSet,
    base_name='geo-rooms'
)
v1.register(
    r'geo/roomcategory',
    geo.RoomCategoryViewSet,
    base_name='geo-roomcategory'
)
v1.register(
    r'geo/doors',
    geo.DoorViewSet,
    base_name='geo-doors'
)
v1.register(
    r'geo/floors',
    geo.FloorViewSet,
    base_name='geo-floors'
)
v1.register(
    r'geo/buildings',
    geo.BuildingViewSet,
    base_name='geo-buildings'
)
v1.register(
    r'geo/nodes',
    geo.NodeViewSet,
    base_name='geo-nodes'
)
v1.register(
    r'geo/edgecategory',
    geo.EdgeCategoryViewSet,
    base_name='geo-edgecategory'
)
v1.register(
    r'geo/edges',
    geo.EdgeViewSet,
    base_name='geo-edges'
)
v1.register(
    r'geo/pointofinterest',
    geo.PointOfInterestViewSet,
    base_name='geo-pointofinterest'
)
v1.register(
    r'geo/pointofinterestinstance',
    geo.PointOfInterestInstanceViewSet,
    base_name='geo-pointofinterestinstance'
)
v1.register(
    r'geo/routing/edges',
    geo.RoutingEdgeViewSet,
    base_name='geo-routing-edge'
)
v1.register(
    r'geo/search/rooms',
    geo.RoomSearchViewSet,
    base_name='geo-room-search'
)
v1.register(
    r'structure/organization',
    structure.OrganizationViewSet,
    base_name='structure-organization'
)
v1.register(
    r'structure/person',
    structure.PersonViewSet,
    base_name='structure-person'
)
v1.register(
    r'attendance/terminal',
    attendance.TerminalViewSet,
    base_name='attendance-terminal'
)
v1.register(
    r'attendance/holding',
    attendance.HoldingViewSet,
    base_name='attendance-holding'
)
v1.register(
    r'attendance/entry',
    attendance.EntryViewSet,
    base_name='attendance-entry'
)
v1.register(
    r'attendance/clock',
    attendance.ClockViewSet,
    base_name='attendance-clock'
)
v1.register(
    r'networktoken/token',
    networktoken.TokenViewSet,
    base_name='networktoken-token'
)
v1.register(
    r'typo3/language',
    typo3.LanguageViewSet,
    base_name='typo3-language'
)
v1.register(
    r'typo3/category',
    typo3.CategoryViewSet,
    base_name='typo3-category'
)
v1.register(
    r'typo3/calendar',
    typo3.CalendarViewSet,
    base_name='typo3-calendar'
)
v1.register(
    r'typo3/eventcategory',
    typo3.EventCategoryViewSet,
    base_name='typo3-eventcategory'
)
v1.register(
    r'typo3/event',
    typo3.EventViewSet,
    base_name='typo3-event'
)
v1.register(
    r'typo3/search/event',
    typo3.EventSearchViewSet,
    base_name='typo3-event-search'
)
v1.register(
    r'typo3/news',
    typo3.NewsViewSet,
    base_name='typo3-news'
)
v1.register(
    r'typo3/search/news',
    typo3.NewsSearchViewSet,
    base_name='typo3-news-search'
)
v1.register(
    r'video/exportclass',
    video.ExportClassViewSet,
    base_name='video-exportclass'
)
v1.register(
    r'video/recorder',
    video.RecorderViewSet,
    base_name='video-recorder'
)
v1.register(
    r'video/epiphan',
    video.EpiphanViewSet,
    base_name='video-epiphan'
)
v1.register(
    r'video/epiphanchannel',
    video.EpiphanChannelViewSet,
    base_name='video-epiphanchannel'
)
v1.register(
    r'video/epiphansource',
    video.EpiphanSourceViewSet,
    base_name='video-epiphansource'
)
v1.register(
    r'video/recording',
    video.RecordingViewSet,
    base_name='video-recording'
)
v1.register(
    r'video/recordingasset',
    video.RecordingAssetViewSet,
    base_name='video-recordingasset'
)
v1.register(
    r'campusonline/room',
    campusonline.RoomViewSet,
    base_name='campusonline-room'
)
v1.register(
    r'campusonline/function',
    campusonline.FunctionViewSet,
    base_name='campusonline-function'
)
v1.register(
    r'campusonline/organization',
    campusonline.OrganizationViewSet,
    base_name='campusonline-organization'
)
v1.register(
    r'campusonline/person',
    campusonline.PersonViewSet,
    base_name='campusonline-person'
)
v1.register(
    r'campusonline/personorganizationfunction',
    campusonline.PersonOrganizationFunctionViewSet,
    base_name='campusonline-personorganizationfunction'
)
v1.register(
    r'campusonline/distributionlist',
    campusonline.DistributionListViewSet,
    base_name='campusonline-distributionlist'
)
v1.register(
    r'campusonline/event',
    campusonline.EventViewSet,
    base_name='campusonline-event'
)
v1.register(
    r'campusonline/bulletin/page',
    campusonline.BulletinPageViewSet,
    base_name='campusonline-bulletin-page'
)
v1.register(
    r'campusonline/bulletin',
    campusonline.BulletinViewSet,
    base_name='campusonline-bulletin'
)
v1.register(
    r'campusonline/search/bulletin.page',
    campusonline.BulletinPageSearchViewSet,
    base_name='campusonline-search-bulletin-page'
)
v1.register(
    r'campusonline/course-group-term',
    campusonline.CourseGroupTermViewSet,
    base_name='campusonline-course-group-term'
)
v1.register(
    r'salt/host',
    salt.HostViewSet,
    base_name='salt-host'
)
v1.register(
    r'thesis/doctoralschool',
    thesis.DoctoralSchoolViewSet,
    base_name='thesis-doctoralschool'
)
v1.register(
    r'thesis/discipline',
    thesis.DisciplineViewSet,
    base_name='thesis-discipline'
)
v1.register(
    r'thesis/thesis',
    thesis.ThesisViewSet,
    base_name='thesis-thesis'
)
v1.register(
    r'thesis/search/thesis',
    thesis.ThesisSearchViewSet,
    base_name='thesis-thesis-search'
)
#v1.register(
#    r'research/country',
#    research.CountryViewSet,
#    base_name='research-country'
#)
#v1.register(
#    r'research/language',
#    research.LanguageViewSet,
#    base_name='research-language'
#)
#v1.register(
#    r'research/funder.category',
#    research.FunderCategoryViewSet,
#    base_name='research-funder-category'
#)
#v1.register(
#    r'research/funder',
#    research.FunderViewSet,
#    base_name='research-funder'
#)
#v1.register(
#    r'research/project.category',
#    research.ProjectCategoryViewSet,
#    base_name='research-project-category'
#)
#v1.register(
#    r'research/project.research',
#    research.ProjectResearchViewSet,
#    base_name='research-project-research'
#)
#v1.register(
#    r'research/project.partnerfunction',
#    research.ProjectPartnerFunctionViewSet,
#    base_name='research-project-partner-function'
#)
#v1.register(
#    r'research/project.study',
#    research.ProjectStudyViewSet,
#    base_name='research-project-study'
#)
#v1.register(
#    r'research/project.event',
#    research.ProjectEventViewSet,
#    base_name='research-project-event'
#)
#v1.register(
#    r'research/project.grant',
#    research.ProjectGrantViewSet,
#    base_name='research-project-grant'
#)
#v1.register(
#    r'research/project.status',
#    research.ProjectStatusViewSet,
#    base_name='research-project-status'
#)
#v1.register(
#    r'research/project',
#    research.ProjectViewSet,
#    base_name='research-project'
#)
#v1.register(
#    r'research/search/project',
#    research.ProjectSearchViewSet,
#    base_name='research-project-search'
#)
#v1.register(
#    r'research/publication.category',
#    research.PublicationCategoryViewSet,
#    base_name='research-publication-category'
#)
#v1.register(
#    r'research/publication.document',
#    research.PublicationDocumentViewSet,
#    base_name='research-publication-document'
#)
v1.register(
    r'research/publication',
    research.PublicationViewSet,
    base_name='research-publication'
)
v1.register(
    r'research/search/publication',
    research.PublicationSearchViewSet,
    base_name='research-publication-search'
)
v1.register(
    r'restaurant/diet',
    restaurant.DietViewSet,
    base_name='restaurant-diet'
)
v1.register(
    r'restaurant/restaurant',
    restaurant.RestaurantViewSet,
    base_name='restaurant-restaurant'
)
v1.register(
    r'restaurant/meal',
    restaurant.MealViewSet,
    base_name='restaurant-meal'
)

urlpatterns = [
    url(r'^v1/', include(v1.urls, namespace='v1')),
]