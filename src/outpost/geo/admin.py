from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from reversion.admin import VersionAdmin

from . import models


class SourceEdgeInline(admin.TabularInline):
    model = models.Edge
    fk_name = "source"


class DestinationEdgeInline(admin.TabularInline):
    model = models.Edge
    fk_name = "destination"


@admin.register(models.Room)
class RoomAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('__str__', 'floor', 'campusonline', 'origin')
    inlines = [
        # DoorInline,
        DestinationEdgeInline,
        SourceEdgeInline,
    ]


@admin.register(models.Background)
class BackgroundAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Level)
class LevelAdmin(OrderedModelAdmin):
    list_display = ('__str__', 'move_up_down_links')


@admin.register(models.Edge)
class EdgeAdmin(VersionAdmin, admin.ModelAdmin):
    pass


@admin.register(models.Node)
class NodeAdmin(VersionAdmin, admin.ModelAdmin):
    pass


@admin.register(models.Building)
class BuildingAdmin(VersionAdmin, admin.ModelAdmin):
    pass


@admin.register(models.Floor)
class FloorAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('__str__', 'level', 'campusonline', 'origin')


@admin.register(models.Beacon)
class BeaconAdmin(admin.ModelAdmin):
    pass


class PointOfInterestInstanceInline(admin.TabularInline):
    model = models.PointOfInterestInstance


@admin.register(models.PointOfInterest)
class PointOfInterestAdmin(admin.ModelAdmin):
    inlines = [
        PointOfInterestInstanceInline,
    ]
