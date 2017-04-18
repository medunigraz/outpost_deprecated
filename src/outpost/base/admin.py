from django.contrib import admin

from . import models


@admin.register(models.Icon)
class IconAdmin(admin.ModelAdmin):
    pass
