from rest_flex_fields.views import FlexFieldsMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from outpost.base.decorators import docstring_format

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


@docstring_format(
    model=models.Country.__doc__,
    serializer=serializers.CountrySerializer.__doc__
)
class CountryViewSet(ReadOnlyModelViewSet):
    '''
    List publication categories.

    {model}
    {serializer}
    '''
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.Language.__doc__,
    serializer=serializers.LanguageSerializer.__doc__
)
class LanguageViewSet(ReadOnlyModelViewSet):
    '''
    List publication categories.

    {model}
    {serializer}
    '''
    queryset = models.Language.objects.all()
    serializer_class = serializers.LanguageSerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.FunderCategory.__doc__,
    serializer=serializers.FunderCategorySerializer.__doc__
)
class FunderCategoryViewSet(ReadOnlyModelViewSet):
    '''
    List publication categories.

    {model}
    {serializer}
    '''
    queryset = models.FunderCategory.objects.all()
    serializer_class = serializers.FunderCategorySerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.Funder.__doc__,
    serializer=serializers.FunderSerializer.__doc__
)
class FunderViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List publication categories.

    {model}
    {serializer}
    '''
    queryset = models.Funder.objects.all()
    serializer_class = serializers.FunderSerializer
    permission_classes = (
        AllowAny,
    )
    permit_list_expands = (
        'category',
        'country',
    )


@docstring_format(
    model=models.ProjectCategory.__doc__,
    serializer=serializers.ProjectCategorySerializer.__doc__
)
class ProjectCategoryViewSet(ReadOnlyModelViewSet):
    '''
    List publication categories.

    {model}
    {serializer}
    '''
    queryset = models.ProjectCategory.objects.all()
    serializer_class = serializers.ProjectCategorySerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.ProjectResearch.__doc__,
    serializer=serializers.ProjectResearchSerializer.__doc__
)
class ProjectResearchViewSet(ReadOnlyModelViewSet):
    '''
    List publication categories.

    {model}
    {serializer}
    '''
    queryset = models.ProjectResearch.objects.all()
    serializer_class = serializers.ProjectResearchSerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.ProjectPartnerFunction.__doc__,
    serializer=serializers.ProjectPartnerFunctionSerializer.__doc__
)
class ProjectPartnerFunctionViewSet(ReadOnlyModelViewSet):
    '''
    List publication categories.

    {model}
    {serializer}
    '''
    queryset = models.ProjectPartnerFunction.objects.all()
    serializer_class = serializers.ProjectPartnerFunctionSerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.ProjectStudy.__doc__,
    serializer=serializers.ProjectStudySerializer.__doc__
)
class ProjectStudyViewSet(ReadOnlyModelViewSet):
    '''
    List publication categories.

    {model}
    {serializer}
    '''
    queryset = models.ProjectStudy.objects.all()
    serializer_class = serializers.ProjectStudySerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.ProjectEvent.__doc__,
    serializer=serializers.ProjectEventSerializer.__doc__
)
class ProjectEventViewSet(ReadOnlyModelViewSet):
    '''
    List publication categories.

    {model}
    {serializer}
    '''
    queryset = models.ProjectEvent.objects.all()
    serializer_class = serializers.ProjectEventSerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.ProjectGrant.__doc__,
    serializer=serializers.ProjectGrantSerializer.__doc__
)
class ProjectGrantViewSet(ReadOnlyModelViewSet):
    '''
    List publication categories.

    {model}
    {serializer}
    '''
    queryset = models.ProjectGrant.objects.all()
    serializer_class = serializers.ProjectGrantSerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.ProjectStatus.__doc__,
    serializer=serializers.ProjectStatusSerializer.__doc__
)
class ProjectStatusViewSet(ReadOnlyModelViewSet):
    '''
    List publication categories.

    {model}
    {serializer}
    '''
    queryset = models.ProjectStatus.objects.all()
    serializer_class = serializers.ProjectStatusSerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.Project.__doc__,
    serializer=serializers.ProjectSerializer.__doc__
)
class ProjectViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List publication categories.

    {model}
    {serializer}
    '''
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permission_classes = (
        AllowAny,
    )
    permit_list_expands = (
        'organization',
        'category',
        'partner_function',
        'manager',
        'contact',
        'status',
        'grant',
        'research',
        'event',
        'study',
        'language',
        'funders',
    )


@docstring_format(
    model=models.PublicationCategory.__doc__,
    serializer=serializers.PublicationCategorySerializer.__doc__
)
class PublicationCategoryViewSet(ReadOnlyModelViewSet):
    '''
    List publication categories.

    {model}
    {serializer}
    '''
    queryset = models.PublicationCategory.objects.all()
    serializer_class = serializers.PublicationCategorySerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.PublicationDocument.__doc__,
    serializer=serializers.PublicationDocumentSerializer.__doc__
)
class PublicationDocumentViewSet(ReadOnlyModelViewSet):
    '''
    List publication documents.

    {model}
    {serializer}
    '''
    queryset = models.PublicationDocument.objects.all()
    serializer_class = serializers.PublicationDocumentSerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.Publication.__doc__,
    serializer=serializers.PublicationSerializer.__doc__
)
class PublicationViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List thesis.

    {model}
    {serializer}
    '''
    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer
    permission_classes = (
        AllowAny,
    )
    permit_list_expands = (
        'persons',
        'organizations',
        'category',
        'document',
    )
