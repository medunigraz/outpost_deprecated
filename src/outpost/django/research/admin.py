from django.contrib import admin

from . import models


@admin.register(models.DjangoProjectCategory)
class DjangoProjectCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'public',
    )


@admin.register(models.DjangoProjectStatus)
class DjangoProjectStatusAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'public',
    )
