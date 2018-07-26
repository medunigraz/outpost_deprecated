import django_filters

from .models import CourseGroupTerm, Bulletin


class CourseGroupTermFilter(django_filters.FilterSet):
    person = django_filters.NumberFilter(
        field_name='person__id',
        lookup_expr='exact'
    )
    term = django_filters.NumberFilter(
        field_name='term',
        lookup_expr='exact'
    )
    room = django_filters.NumberFilter(
        field_name='room',
        lookup_expr='exact'
    )
    start__gte = django_filters.IsoDateTimeFilter(
        field_name='start',
        lookup_expr='gte'
    )
    start__gt = django_filters.IsoDateTimeFilter(
        field_name='start',
        lookup_expr='gt'
    )
    start__lte = django_filters.IsoDateTimeFilter(
        field_name='start',
        lookup_expr='lte'
    )
    start__lt = django_filters.IsoDateTimeFilter(
        field_name='start',
        lookup_expr='lt'
    )
    end__gte = django_filters.IsoDateTimeFilter(
        field_name='end',
        lookup_expr='gte'
    )
    end__gt = django_filters.IsoDateTimeFilter(
        field_name='end',
        lookup_expr='gt'
    )
    end__lte = django_filters.IsoDateTimeFilter(
        field_name='end',
        lookup_expr='lte'
    )
    end__lt = django_filters.IsoDateTimeFilter(
        field_name='end',
        lookup_expr='lt'
    )

    class Meta:
        model = CourseGroupTerm
        fields = tuple()


class BulletinFilter(django_filters.FilterSet):
    issue = django_filters.CharFilter(
        field_name='issue',
        lookup_expr='exact'
    )
    academic_year = django_filters.CharFilter(
        field_name='academic_year',
        lookup_expr='contains'
    )
    room = django_filters.NumberFilter(
        field_name='room',
        lookup_expr='exact'
    )
    published__gte = django_filters.IsoDateTimeFilter(
        field_name='published',
        lookup_expr='gte'
    )
    published__gt = django_filters.IsoDateTimeFilter(
        field_name='published',
        lookup_expr='gt'
    )
    published__lte = django_filters.IsoDateTimeFilter(
        field_name='published',
        lookup_expr='lte'
    )
    published__lt = django_filters.IsoDateTimeFilter(
        field_name='published',
        lookup_expr='lt'
    )

    class Meta:
        model = Bulletin
        fields = tuple()
