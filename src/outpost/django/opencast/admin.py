from django.contrib import admin

from . import models


@admin.register(models.GroupMap)
class GroupMapAdmin(admin.ModelAdmin):
    list_display = (
        'group',
        'dn',
        'enabled',
    )
    list_display_links = (
        'group',
    )
    list_filter = (
        'enabled',
    )
