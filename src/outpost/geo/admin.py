from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
    PolymorphicParentModelAdmin,
)
from reversion.admin import VersionAdmin

from . import models


@admin.register(models.Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'campusonline', 'origin')


@admin.register(models.Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'level', 'campusonline', 'origin')
    list_filter = (
        'level',
        'building',
    )


class SourceEdgeInline(admin.TabularInline):
    model = models.Edge
    fk_name = "source"


class DestinationEdgeInline(admin.TabularInline):
    model = models.Edge
    fk_name = "destination"


class NodeChildAdmin(PolymorphicChildModelAdmin):
    base_model = models.Node


@admin.register(models.Node)
class NodeParentAdmin(PolymorphicParentModelAdmin):
    base_model = models.Node
    child_models = (models.Door, models.Room)
    list_filter = (
        PolymorphicChildModelFilter,
        'level',
    )


@admin.register(models.Door)
class DoorAdmin(NodeChildAdmin):
    base_model = models.Door
    list_display = ('__str__', 'level', 'origin')
    list_filter = (
        'level',
    )


@admin.register(models.Room)
class RoomAdmin(NodeChildAdmin):
    base_model = models.Room
    list_display = ('__str__', 'level', 'campusonline', 'origin')
    inlines = [
        DestinationEdgeInline,
        SourceEdgeInline,
    ]
    list_filter = (
        'level',
    )


@admin.register(models.Background)
class BackgroundAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Level)
class LevelAdmin(OrderedModelAdmin):
    list_display = ('__str__', 'move_up_down_links')


@admin.register(models.EdgeCategory)
class EdgeCategoryAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('__str__', 'weight')


@admin.register(models.Edge)
class EdgeAdmin(VersionAdmin, admin.ModelAdmin):
    pass


class PointOfInterestInstanceInline(admin.TabularInline):
    model = models.PointOfInterestInstance


@admin.register(models.PointOfInterest)
class PointOfInterestAdmin(admin.ModelAdmin):
    inlines = [
        PointOfInterestInstanceInline,
    ]
