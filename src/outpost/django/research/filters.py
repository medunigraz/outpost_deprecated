from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import (
    filters,
    filterset,
)

from . import models


class ProjectFilter(filterset.FilterSet):
    '''
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    Possible exact filters:

      - `organization`
      - `category`
      - `manager`
      - `contact`
      - `status`
      - `grant`
      - `research`
      - `study`
      - `language`
      - `funders`
      - `program`

    For advanced filtering use lookups:

        ?<fieldname>__<lookup>=<value>

    All fields with advanced lookups can also be used for exact value matches
    as described above.

    Possible advanced lookups:

      - `begin_planned`: `gt`, `gte`, `lt`, `lte`
      - `begin_effective`: `gt`, `gte`, `lt`, `lte`
      - `end_planned`: `gt`, `gte`, `lt`, `lte`
      - `end_effective`: `gt`, `gte`, `lt`, `lte`
    '''

    class Meta:
        model = models.Project
        fields = {
            'organization': ('exact',),
            'category': ('exact',),
            'manager': ('exact',),
            'contact': ('exact',),
            'status': ('exact',),
            'begin_planned': (
                'exact',
                'gt',
                'lt',
                'gte',
                'lte',
                'date',
            ),
            'begin_effective': (
                'exact',
                'gt',
                'lt',
                'gte',
                'lte',
                'date',
            ),
            'end_planned': (
                'exact',
                'gt',
                'lt',
                'gte',
                'lte',
                'date',
            ),
            'end_effective': (
                'exact',
                'gt',
                'lt',
                'gte',
                'lte',
                'date',
            ),
            'grant': ('exact',),
            'research': ('exact',),
            'event': ('exact',),
            'study': ('exact',),
            'language': ('exact',),
            'funders': ('exact',),
            'assignment': (
                'exact',
                'gt',
                'lt',
                'gte',
                'lte',
                'date',
            ),
            'program': ('exact',),
        }


class PublicationFilter(filterset.FilterSet):
    '''
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    Possible exact filters:

      - `year`
      - `category`
      - `document`
      - `persons`

    For advanced filtering use lookups:

        ?<fieldname>__<lookup>=<value>

    All fields with advanced lookups can also be used for exact value matches
    as described above.

    Possible advanced lookups:

      - `sci`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`
      - `pubmed`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`
      - `doi`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`
      - `pmc`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`
    '''

    class Meta:
        model = models.Publication
        fields = {
            'year': ('exact',),
            'category': ('exact',),
            'document': ('exact',),
            'sci': (
                'exact',
                'iexact',
                'contains',
                'icontains',
                'startswith',
                'istartswith',
            ),
            'pubmed': (
                'exact',
                'iexact',
                'contains',
                'icontains',
                'startswith',
                'istartswith',
            ),
            'doi': (
                'exact',
                'iexact',
                'contains',
                'icontains',
                'startswith',
                'istartswith',
            ),
            'pmc': (
                'exact',
                'iexact',
                'contains',
                'icontains',
                'startswith',
                'istartswith',
            ),
            'persons': ('exact',),
        }
