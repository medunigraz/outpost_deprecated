from drf_haystack.viewsets import HaystackViewSet
from rest_flex_fields.views import FlexFieldsMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import (
    AllowAny,
)

# from rest_framework_extensions.mixins import (
#     CacheResponseAndETAGMixin,
# )
# from rest_framework_extensions.cache.mixins import (
#     CacheResponseMixin,
# )
from . import (
    models,
    serializers,
)
from ..api.permissions import ExtendedDjangoModelPermissions
from ..base.decorators import docstring_format


@docstring_format(
    model=models.DoctoralSchool.__doc__
)
class DoctoralSchoolViewSet(ReadOnlyModelViewSet):
    '''
    List doctoral schools for thesis.

    {model}
    '''
    queryset = models.DoctoralSchool.objects.all()
    serializer_class = serializers.DoctoralSchoolSerializer
    permission_classes = (
        IsAuthenticated,
    )


@docstring_format(
    model=models.Discipline.__doc__
)
class DisciplineViewSet(ReadOnlyModelViewSet):
    '''
    List disciplines for thesis.

    {model}
    '''
    queryset = models.Discipline.objects.all()
    serializer_class = serializers.DisciplineSerializer
    permission_classes = (
        IsAuthenticated,
    )


@docstring_format(
    model=models.Thesis.__doc__,
    serializer=serializers.ThesisSerializer.__doc__
)
class ThesisViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List thesis.

    {model}
    {serializer}
    '''
    queryset = models.Thesis.objects.all()
    serializer_class = serializers.ThesisSerializer
    permission_classes = (
        IsAuthenticated,
        ExtendedDjangoModelPermissions,
    )
    filter_fields = (
        'doctoralschool',
        'discipline',
        'editors',
    )
    permit_list_expands = (
        'doctoralschool',
        'discipline',
        'editors',
    )


class ThesisSearchViewSet(HaystackViewSet):
    index_models = [models.Thesis]
    serializer_class = serializers.ThesisSearchSerializer
    permission_classes = (
        IsAuthenticated,
    )
