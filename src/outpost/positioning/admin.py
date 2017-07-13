from django.contrib import admin

from . import models


@admin.register(models.Beacon)
class BeaconAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'level',
        'deployed',
        'seen',
        'charge',
        'active',
    )
    list_filter = (
        'level',
        'active',
    )
    search_fields = (
        'name',
    )
