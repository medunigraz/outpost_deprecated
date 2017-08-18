from django.contrib import admin
from django.utils.html import linebreaks

from . import models


class RecordingInlineAdmin(admin.TabularInline):
    model = models.Recording


@admin.register(models.Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'fingerprint',
        'active',
    )
    list_filter = (
        'active',
    )
    search_fields = (
        'hostname',
        'port',
    )
    readonly_fields = (
        'fingerprint',
    )

    def fingerprint(self, obj):
        return '<code>{}</code>'.format(obj.fingerprint)
    fingerprint.short_description = u'SSH host key fingerprint'
    fingerprint.allow_tags = True


@admin.register(models.Epiphan)
class EpiphanAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'server',
        'fingerprint',
        'active',
    )
    list_filter = (
        'server',
        'active',
    )
    search_fields = (
        'name',
        'hostname',
        'fingerprint',
    )
    readonly_fields = (
        'fingerprint',
        'private_key',
    )
    inlines = (
        RecordingInlineAdmin,
    )

    def fingerprint(self, obj):
        return '<code>{}</code>'.format(obj.fingerprint)
    fingerprint.short_description = u'SSH public key fingerprint'
    fingerprint.allow_tags = True

    def private_key(self, obj):
        return '<pre>{}</pre>'.format(obj.private_key)
    private_key.short_description = u'SSH private key'
    private_key.allow_tags = True


#class EventInlineAdmin(admin.TabularInline):
#    model = models.Event
#
#
#@admin.register(models.Series)
#class SeriesAdmin(admin.ModelAdmin):
#    inlines = (
#            EventInlineAdmin,
#    )
#
#
#@admin.register(models.Event)
#class EventAdmin(admin.ModelAdmin):
#    pass
