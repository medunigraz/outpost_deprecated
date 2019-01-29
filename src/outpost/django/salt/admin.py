from django.contrib import admin

from . import models


class PublicKeyInline(admin.TabularInline):
    model = models.PublicKey


class SystemUserInline(admin.TabularInline):
    model = models.SystemUser


@admin.register(models.System)
class SystemAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
    )
    inlines = (
        SystemUserInline,
    )


@admin.register(models.Host)
class HostAdmin(admin.ModelAdmin):
    list_filter = (
        'system',
    )
    search_fields = (
        'name',
    )


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    inlines = (
        SystemUserInline,
        PublicKeyInline,
    )
    list_display = (
        'pk',
        'username',
        'person',
        'email',
    )
    list_filter = (
        'systems',
    )
    search_fields = (
        'person__username',
        'person__first_name',
        'person__last_name',
        'person__email',
    )


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    pass
