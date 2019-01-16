from django.contrib import admin

from . import models


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'office',
        'hidden',
    )
    search_fields = (
        'name',
        'campusonline__name',
    )


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'hidden',
    )
    search_fields = (
        'campusonline__first_name',
        'campusonline__last_name',
    )
