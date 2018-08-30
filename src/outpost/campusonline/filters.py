import django_filters
from django.utils.translation import gettext_lazy as _

from .models import (
    Bulletin,
    CourseGroupTerm,
    Function,
    Person,
)


class PersonFilter(django_filters.FilterSet):
    '''
    Filters
    -------

    To filter for exact value matches:

        ?<fieldname>=<value>

    For advanced filtering use lookups:

        ?<fieldname>__<lookup>=<value>

    Possible lookups:

      - `first_name`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`, `endswith`, `iendswith`, `isnull`, `regex`, `iregex`
      - `last_name`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`, `endswith`, `iendswith`, `isnull`, `regex`, `iregex`
      - `title`: `iexact`, `contains`, `icontains`, `isnull`, `regex`, `iregex`
      - `consultation`: `contains`, `icontains`, `isnull`, `regex`, `iregex`
      - `appendix`: `contains`, `icontains`, `isnull`, `regex`, `iregex`
    '''
    sex = django_filters.ChoiceFilter(
        label=_('Sex'),
        choices=Person.GENDER_CHOICES
    )
    functions = django_filters.ModelMultipleChoiceFilter(
        label=_('Function'),
        queryset=Function.objects.all()
    )

    class Meta:
        model = Person
        fields = {
            'first_name': (
                'exact',
                'iexact',
                'contains',
                'icontains',
                'startswith',
                'istartswith',
                'endswith',
                'iendswith',
                'isnull',
                'regex',
                'iregex',
            ),
            'last_name': (
                'exact',
                'iexact',
                'contains',
                'icontains',
                'startswith',
                'istartswith',
                'endswith',
                'iendswith',
                'isnull',
                'regex',
                'iregex',
            ),
            'title': (
                'exact',
                'iexact',
                'contains',
                'icontains',
                'isnull',
                'regex',
                'iregex',
            ),
            'consultation': (
                'contains',
                'icontains',
                'isnull',
                'regex',
                'iregex',
            ),
            'appendix': (
                'contains',
                'icontains',
                'isnull',
                'regex',
                'iregex',
            ),
        }


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
    start__date = django_filters.DateFilter(
        field_name='start',
        lookup_expr='date'
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
    end__date = django_filters.DateFilter(
        field_name='end',
        lookup_expr='date'
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
