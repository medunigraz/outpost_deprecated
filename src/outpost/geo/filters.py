from functools import reduce

import django_filters
from django.db.models import Q

from . import models


class EdgeFilter(django_filters.FilterSet):
    floor = django_filters.NumberFilter(
        action=lambda q, v: EdgeFilter.filter_floor(q, v)
    )
    source_floor = django_filters.NumberFilter(
        name='source__floor'
    )
    destination_floor = django_filters.NumberFilter(
        name='destination__floor'
    )

    class Meta:
        model = models.Edge

    @staticmethod
    def filter_floor(queryset, value):
        fields = [
            'source__floor__exact',
            'destination__floor__exact',
        ]
        floors = reduce(
            lambda x, y: x | y,
            [Q(**{field: value}) for field in fields]
        )
        return queryset.filter(floors)
