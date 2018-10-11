from django.contrib import admin

from . import models


class PersonInline(admin.TabularInline):
    model = models.Person.distribution_list_internal.through


@admin.register(models.DistributionListInternal)
class DistributionListInternalAdmin(admin.ModelAdmin):
    inlines = [
        PersonInline,
    ]
