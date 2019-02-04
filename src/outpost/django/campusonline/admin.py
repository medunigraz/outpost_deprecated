from django.contrib import admin

from . import models


class PersonInline(admin.TabularInline):
    model = models.Person.distribution_list_internal.through


@admin.register(models.DistributionListInternal)
class DistributionListInternalAdmin(admin.ModelAdmin):
    inlines = [
        PersonInline,
    ]


@admin.register(models.BulletinPage)
class BulletinPageAdmin(admin.ModelAdmin):
    list_display = (
        'bulletin',
        'index',
        'clean',
    )
    list_display_links = (
        'index',
    )
    list_filter = (
        'clean',
    )
    readonly_fields = (
        'bulletin',
        'index',
    )
