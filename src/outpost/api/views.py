from drf_haystack.viewsets import HaystackViewSet
from drf_haystack.filters import HaystackAutocompleteFilter
from rest_framework.permissions import (
    AllowAny,
)
from . import (
    serializers,
)

from ..geo import models as geo
from ..structure import models as structure


class AutocompleteViewSet(HaystackViewSet):
    """
    Get autocomplete suggestions for geographic objects:

        .../?q=<Word>

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
