from django.contrib import admin

from . import models


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'hidden',
    )


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'hidden',
    )
