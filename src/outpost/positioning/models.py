import logging

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

from netfields import MACAddressField

logger = logging.getLogger(__name__)


class Beacon(models.Model):
    mac = MACAddressField(
        primary_key=True,
        db_index=True
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
        max_digits=5,
        decimal_places=2
    )

    def __str__(self):
        return '{s.mac} ({s.level})'.format(s=self)


class AccessPoint(models.Model):
    mac = MACAddressField(
        primary_key=True,
        db_index=True
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
