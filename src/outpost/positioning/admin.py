from django.contrib import admin

from . import models


@admin.register(models.Beacon)
class BeaconAdmin(admin.ModelAdmin):
    pass
