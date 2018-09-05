from django.contrib import admin

from . import models


@admin.register(models.Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'terminal',
        'created',

    )
    list_filter = (
        'terminal',
    )
    search_fields = (
        'student__first_name',
        'student__last_name',
        'terminal__room__name',
        'terminal__room__campusonline__title',
        'terminal__hostname',
    )
    date_hierarchy = 'created'


@admin.register(models.Terminal)
class TerminalAdmin(admin.ModelAdmin):
    list_display = (
        'hostname',
        'room',
        'enabled',
        'online',
    )
    list_filter = (
        'enabled',
        'online',
    )
    search_fields = (
        'room__name',
        'room__campusonline__title',
        'hostname',
    )


class CampusOnlineEntryInline(admin.TabularInline):
    model = models.CampusOnlineEntry


@admin.register(models.CampusOnlineHolding)
class CampusOnlineHoldingAdmin(admin.ModelAdmin):
    inlines = [
        CampusOnlineEntryInline,
    ]


class StatisticsEntryInline(admin.TabularInline):
    model = models.StatisticsEntry


@admin.register(models.Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    inlines = [
        StatisticsEntryInline,
    ]
