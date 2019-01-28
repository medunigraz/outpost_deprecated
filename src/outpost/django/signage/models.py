import reversion
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
from django.contrib.gis.geos import (
    LineString,
    Point,
)
from django.db.models import Q
from django_extensions.db.models import TimeStampedModel
from ordered_model.models import OrderedModel
from polymorphic.models import PolymorphicModel

from outpost.base.decorators import signal_connect
from outpost.base.fields import LowerCaseCharField
from outpost.base.key_constructors import UpdatedAtKeyBit
from outpost.base.models import NetworkedDeviceMixin


class Client(NetworkedDeviceMixin, PolymorphicModel):
    id = models.CharField(
        max_length=32,
        readonly=True,
        primary_key=True,
    )
    name = models.CharField(max_length=128, blank=False, null=False)
    username = models.CharField(max_length=128, blank=False, null=False)
    key = models.BinaryField(null=False)
    provision = models.BooleanField(default=False)
    room = models.ForeignKey(
        'geo.Room',
        null=True,
        blank=True
    )
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    dpi = models.PositiveIntegerField(null=True, blank=True)
    schedule = models.ForeignKey(
        'Schedule',
        null=True,
        blank=True,
    )


class ClientResolution(models.Model):
    client = models.ForeignKey(
        'Client'
    )
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()


class Group(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    clients = models.ManyToManyField('Client')


class Content(TimeStampedModel, PolymorphicModel):
    name = models.CharField(max_length=128, blank=False, null=False)


class CampusOnlineEventContent(Content):
    building = models.





class Schedule(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    default = models.ForeignKey('Content')


class ScheduleItem(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    content = models.ForeignKey('Content')
