from functools import reduce

import django_filters
from django.db.models import Q

from . import models


class BuildingFilter(django_filters.FilterSet):

    class Meta:
        model = models.Building
        fields = [
            'campusonline',
        ]


class FloorFilter(django_filters.FilterSet):

    class Meta:
        model = models.Floor
        fields = [
            'level',
            'campusonline',
        ]


class NodeFilter(django_filters.FilterSet):
    level = django_filters.ModelChoiceFilter(
        name='floor__level',
        queryset=models.Level.objects.all()
    )

    class Meta:
        model = models.Node
        fields = [
            'level',
        ]


class RoomFilter(NodeFilter):

    class Meta(NodeFilter.Meta):
        model = models.Room
        fields = [
            'campusonline',
            'category',
        ] + NodeFilter.Meta.fields


class DoorFilter(NodeFilter):

    class Meta(NodeFilter.Meta):
        model = models.Door


class PointOfInterestInstanceFilter(NodeFilter):

    class Meta(NodeFilter.Meta):
        model = models.PointOfInterestInstance
        fields = [
            'name',
        ] + NodeFilter.Meta.fields


class EdgeFilter(django_filters.FilterSet):
    level = django_filters.NumberFilter(
        action=lambda q, v: EdgeFilter.filter_level(q, v)
    )
    source_level = django_filters.NumberFilter(
        name='source__floor__level'
    )
    destination_level = django_filters.NumberFilter(
        name='destination__floor__level'
    )

    class Meta:
        model = models.Edge

    @staticmethod
    def filter_level(queryset, value):
        fields = [
            'source__floor__level__exact',
            'destination__floor__level__exact',
        ]
        floors = reduce(
            lambda x, y: x | y,
            [Q(**{field: value}) for field in fields]
        )
        return queryset.filter(floors)
