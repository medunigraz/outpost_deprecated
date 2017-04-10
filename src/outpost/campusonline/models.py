from django.contrib.gis.db import models


class RoomCategory(models.Model):
    id = models.IntegerField(
        primary_key=True
    )
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'campusonline_room_category'


class Room(models.Model):
    id = models.IntegerField(
        primary_key=True
    )
    title = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    building = models.ForeignKey(
        'Building',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    floor = models.ForeignKey(
        'Floor',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    name_short = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    name_full = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    area = models.DecimalField(
        max_digits=65535,
        decimal_places=1,
        blank=True,
        null=True
    )
    height = models.DecimalField(
        max_digits=65535,
        decimal_places=1,
        blank=True,
        null=True
    )
    organization = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        'RoomCategory',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )

    class Meta:
        managed = False
        db_table = 'campusonline_room'


class Floor(models.Model):
    id = models.IntegerField(
        primary_key=True
    )
    short = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'campusonline_floor'


class Building(models.Model):
    id = models.IntegerField(
        primary_key=True
    )
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    short = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )
    address = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'campusonline_building'

