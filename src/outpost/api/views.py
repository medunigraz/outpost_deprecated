from drf_haystack.filters import HaystackAutocompleteFilter
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.permissions import AllowAny

from . import serializers
from ..geo import models as geo
from ..structure import models as structure


class AutocompleteViewSet(HaystackViewSet):
    """
    Get autocomplete suggestions for geographic objects:

        .../?q=<Word>

    To limit results to certain models use the `m` parameter:

        .../?q=<Word>&m=<Model>,<Model>,...

    Possible models are currently:

     * `geo.Room`
     * `structure.Organization`
     * `structure.Person`

    The `ctype` property determines the content type of each suggested item.
    This can be used to do further queries at other endpoints.
    """
    serializer_class = serializers.AutocompleteSerializer
    index_models = (
        geo.Room,
        structure.Organization,
        structure.Person,
    )
    permission_classes = (
        AllowAny,
    )
    filter_backends = (
        HaystackAutocompleteFilter,
    )

    def get_queryset(self, index_models=[]):
        queryset = self.object_class()._clone()
        if 'm' in self.request.GET:
            allowed = self.request.GET.get('m').split(',')
            models = filter(
                lambda m: m._meta.label in allowed,
                self.index_models
            )
            queryset = queryset.models(*models)
        else:
            queryset = queryset.models(*self.index_models)
        return queryset
