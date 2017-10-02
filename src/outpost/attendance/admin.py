from django.contrib import admin

from . import models


class EntryInline(admin.TabularInline):
    model = models.Entry


@admin.register(models.Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'state',
        'holding',
        'room',
    )
    list_filter = (
        'state',
    )
    search_fields = (
        'student__first_name',
        'student__last_name',
        'room__title',
    )
    date_hierarchy = 'registered'


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


@admin.register(models.Holding)
class HoldingAdmin(admin.ModelAdmin):
    inlines = [
        EntryInline,
    ]
