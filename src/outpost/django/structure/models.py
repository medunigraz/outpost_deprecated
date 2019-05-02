from django.db import models

from outpost.django.base.fields import LowerCaseCharField
from outpost.django.base.models import RelatedManager


class Organization(models.Model):
    name = models.CharField(
        max_length=128,
        blank=True,
        null=True
    )
    campusonline = models.ForeignKey(
        'campusonline.Organization',
        models.CASCADE,
        db_constraint=False,
        related_name='+',
        blank=True,
        null=True
    )
    color = LowerCaseCharField(
        max_length=6,
        default='007b3c'
    )
    office = models.ForeignKey(
        'geo.Room',
        null=True,
        blank=True,
        related_name='+'
    )
    hidden = models.BooleanField(
        default=False
    )

    objects = RelatedManager(
        select=(
            'campusonline',
            'office',
        ),
        prefetch=(
            'campusonline__persons',
            'campusonline__publication_authorship',
            'office__campusonline',
        )
    )

    class Meta:
        ordering = (
            'campusonline__name',
        )

    def __str__(self):
        if self.campusonline and not self.name:
            return self.campusonline.name
        return self.name


class Person(models.Model):
    campusonline = models.ForeignKey(
        'campusonline.Person',
        models.CASCADE,
        db_constraint=False,
        related_name='+'
    )
    room = models.ForeignKey(
        'geo.Room',
        null=True,
        blank=True
    )
    hidden = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = (
            'campusonline__last_name',
            'campusonline__first_name',
        )

    def __str__(self):
        return '{c.last_name}, {c.first_name}'.format(c=self.campusonline)
