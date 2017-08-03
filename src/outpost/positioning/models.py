import logging

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from netfields import MACAddressField

logger = logging.getLogger(__name__)


class Beacon(models.Model):
    name = models.CharField(
        max_length=16,
        db_index=True,
        unique=True
    )
    level = models.ForeignKey('geo.Level')
    position = models.PointField(
        srid=settings.DEFAULT_SRID
    )
    deployed = models.DateTimeField(
        auto_now_add=True
    )
    seen = models.DateTimeField(
        auto_now_add=True
    )
    active = models.BooleanField(
        default=False
    )
    charge = models.DecimalField(
        null=True,
        default=0,
        max_digits=5,
        decimal_places=2
    )

    def __str__(self):
        return '{s.name} ({s.level})'.format(s=self)


class AccessPoint(models.Model):
    mac = models.CharField(
        max_length=17,
        db_index=True,
        unique=True
    )
    level = models.ForeignKey('geo.Level')
    position = models.PointField(
        srid=settings.DEFAULT_SRID
    )
    seen = models.DateTimeField(
        auto_now_add=True
    )
    active = models.BooleanField(
        default=False,
    )
