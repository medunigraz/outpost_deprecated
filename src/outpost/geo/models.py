from django.conf import settings
from django.contrib.gis.db import models
from ordered_model.models import OrderedModel
from polymorphic.models import PolymorphicModel

from outpost.base.decorators import signal_connect


class Building(models.Model):
    name = models.TextField()
    outline = models.MultiPolygonField(
        null=True,
        blank=True,
        srid=settings.DEFAULT_SRID
    )
    campusonline = models.ForeignKey(
        'campusonline.Building',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )

    def __str__(self):
        return self.name


class Floor(OrderedModel):
    name = models.TextField()
    building = models.ForeignKey('Building')
    campusonline = models.ForeignKey(
        'campusonline.Floor',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )

    class Meta(OrderedModel.Meta):
        pass

    def __str__(self):
        return '{s.name} ({s.building})'.format(s=self)


class Node(PolymorphicModel):
    floor = models.ForeignKey('Floor')
    center = models.PointField(srid=settings.DEFAULT_SRID)

    def __str__(self):
        return 'Node at {s.floor}'.format(s=self)


class Edge(models.Model):
    source = models.ForeignKey(
        'node',
        related_name='edges_source'
    )
    destination = models.ForeignKey(
        'node',
        related_name='edges_destination'
    )
    one_way = models.BooleanField(default=False)
    accessible = models.BooleanField(default=False)
    weight = models.IntegerField(default=1)
    path = models.LineStringField(srid=settings.DEFAULT_SRID)
    door = models.ForeignKey(
        'Door',
        null=True,
        blank=True
    )

    def __str__(self):
        return 'Edge between {s.source} and {s.destination}'.format(s=self)


class RoomCategory(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name or 'Undefined'


@signal_connect
class Room(Node):
    layout = models.PolygonField(
        srid=settings.DEFAULT_SRID
    )
    virtual = models.BooleanField(
        default=False
    )
    category = models.ForeignKey(
        'RoomCategory',
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    campusonline = models.ForeignKey(
        'campusonline.Room',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )

    def __str__(self):
        return self.name or 'Room'

    def pre_save(self, *args, **kwargs):
        if self.layout:
            self.center = self.layout.point_on_surface


class Walls(models.Model):
    floor = models.ForeignKey('Floor')
    lines = models.MultiLineStringField(
        srid=settings.DEFAULT_SRID
    )


class Door(Node):
    rooms = models.ManyToManyField(
        'Room'
    )


class Beacon(models.Model):
    uuid = models.UUIDField()
    major = models.PositiveIntegerField()
    minor = models.PositiveIntegerField()
    floor = models.ForeignKey('Floor')
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
