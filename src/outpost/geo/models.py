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


class OriginMixin(models.Model):
    origin = models.IntegerField(null=True)

    class Meta:
        abstract = True


class Background(models.Model):
    name = models.CharField(max_length=16)
    outline = models.MultiPolygonField(
        null=True,
        blank=True,
        srid=settings.DEFAULT_SRID
    )

    def __str__(self):
        return self.name


@reversion.register()
class Level(OrderedModel):
    name = models.CharField(max_length=16)

    class Meta(OrderedModel.Meta):
        pass

    def __str__(self):
        return self.name


@signal_connect
@reversion.register()
class Building(OriginMixin, models.Model):
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
        if not self.campusonline:
            return self.name or 'Building'
        return '{s.name} [CO: {s.campusonline}]'.format(s=self)

    def post_save(self, *args, **kwargs):
        UpdatedAtKeyBit.update(self)

    def post_delete(self, *args, **kwargs):
        UpdatedAtKeyBit.update(self)


@signal_connect
@reversion.register()
class Floor(OriginMixin, models.Model):
    name = models.TextField()
    building = models.ForeignKey('Building')
    level = models.ForeignKey('Level', null=True)
    outline = models.MultiPolygonField(
        null=True,
        blank=True,
        srid=settings.DEFAULT_SRID
    )
    campusonline = models.ForeignKey(
        'campusonline.Floor',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )

    def __str__(self):
        return '{s.name} ({s.building})'.format(s=self)

    def post_save(self, *args, **kwargs):
        UpdatedAtKeyBit.update(self)

    def post_delete(self, *args, **kwargs):
        UpdatedAtKeyBit.update(self)


@signal_connect
@reversion.register()
class Node(TimeStampedModel, PolymorphicModel):
    level = models.ForeignKey('Level')
    center = models.PointField(srid=settings.DEFAULT_SRID)
    deprecated = models.BooleanField(default=False)

    def __str__(self):
        return '{t} at {s.level}'.format(
            t=ContentType.objects.get_for_id(self.polymorphic_ctype_id),
            s=self
        )

    def post_save(self, *args, **kwargs):
        for e in Edge.objects.filter(Q(source=self) | Q(destination=self)):
            e.save()
        UpdatedAtKeyBit.update(self)

    def post_delete(self, *args, **kwargs):
        UpdatedAtKeyBit.update(self)


@reversion.register()
class EdgeCategory(models.Model):
    name = models.CharField(
        max_length=64
    )
    multiplicator = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=1.0
    )
    addition = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=0
    )

    class Meta:
        ordering = ('multiplicator', 'addition')

    def __str__(self):
        return self.name or 'Undefined'


@signal_connect
@reversion.register()
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
    category = models.ForeignKey(
        'EdgeCategory'
    )
    path = models.LineStringField(srid=settings.DEFAULT_SRID)

    def __str__(self):
        return 'Edge between {s.source} and {s.destination}'.format(s=self)

    def pre_save(self, *args, **kwargs):
        self.path = LineString(self.source.center, self.destination.center)

    def post_save(self, *args, **kwargs):
        UpdatedAtKeyBit.update(self)

    def post_delete(self, *args, **kwargs):
        UpdatedAtKeyBit.update(self)


@reversion.register()
class RoomCategory(models.Model):
    name = models.TextField()
    searchable = models.BooleanField(default=True)
    campusonline = models.ForeignKey(
        'campusonline.RoomCategory',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )

    def __str__(self):
        return self.name or 'Undefined'


@signal_connect
@reversion.register(follow=['node_ptr'])
class Room(OriginMixin, Node):
    layout = models.PolygonField(
        srid=settings.DEFAULT_SRID
    )
    marker = models.PointField(
        srid=settings.DEFAULT_SRID,
        default=Point(0, 0)
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
    organization = models.ForeignKey(
        'structure.Organization',
        null=True,
        blank=True
    )

    def __str__(self):
        if self.name:
            return self.name
        if self.campusonline:
            return str(self.campusonline)
        return '-'

    def pre_save(self, *args, **kwargs):
        if self.layout:
            self.center = self.layout.point_on_surface

            def x(k): return k[0]

            def y(k): return k[1]

            # Map all [(x,y)] to [y] and select the maximum
            # Filter all [(x,y)] where y = max_y
            # Select maximum y from [(x,y)] and save as marker anchor point
            c = self.layout.coords
            max_y = max(map(lambda k: y(k), c[0]))
            self.marker = Point(min(filter(lambda k: y(k) == max_y, c[0]), key=lambda k: x(k)), srid=settings.DEFAULT_SRID)

    def post_save(self, *args, **kwargs):
        super().post_save(*args, **kwargs)

    def post_delete(self, *args, **kwargs):
        super().post_delete(*args, **kwargs)


@signal_connect
@reversion.register(follow=['node_ptr'])
class Door(OriginMixin, Node):
    rooms = models.ManyToManyField(
        'Room'
    )
    layout = models.PolygonField(
        srid=settings.DEFAULT_SRID
    )

    def pre_save(self, *args, **kwargs):
        if self.layout:
            self.center = self.layout.centroid

    def post_save(self, *args, **kwargs):
        super().post_save(*args, **kwargs)

    def post_delete(self, *args, **kwargs):
        super().post_delete(*args, **kwargs)


@signal_connect
@reversion.register()
class PointOfInterest(OrderedModel):
    name = models.CharField(
        max_length=128
    )
    color = LowerCaseCharField(
        max_length=6,
        default='007b3c'
    )
    selected = models.BooleanField(
        default=False
    )
    font_key = models.CharField(
        max_length=1
    )
    css_class = models.CharField(
        max_length=128
    )

    class Meta(OrderedModel.Meta):
        pass

    def __str__(self):
        return self.name

    def post_save(self, *args, **kwargs):
        UpdatedAtKeyBit.update(self)

    def post_delete(self, *args, **kwargs):
        UpdatedAtKeyBit.update(self)


@signal_connect
@reversion.register(follow=['node_ptr'])
class PointOfInterestInstance(Node):
    name = models.ForeignKey('PointOfInterest')
    description = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.name)

    def post_save(self, *args, **kwargs):
        super().post_save(*args, **kwargs)

    def post_delete(self, *args, **kwargs):
        super().post_delete(*args, **kwargs)
