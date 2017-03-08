from django.contrib import admin

from . import models


class EntryInline(admin.TabularInline):
    model = models.Entry


@admin.register(models.Holding)
class HoldingAdmin(admin.ModelAdmin):
    inlines = [
        EntryInline,
    ]


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [
        EntryInline,
    ]
