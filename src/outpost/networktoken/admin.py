from django.contrib import admin

from . import models


@admin.register(models.Token)
class EntryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'created',
        'lifetime',
        'value',
    )
    list_filter = (
        'user',
    )
    search_fields = (
        'user',
    )
