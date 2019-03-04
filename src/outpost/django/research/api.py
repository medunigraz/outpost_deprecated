from django_filters.rest_framework import DjangoFilterBackend
from drf_haystack.viewsets import HaystackViewSet
from rest_flex_fields.views import FlexFieldsMixin
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

# from rest_framework_extensions.mixins import (
#     CacheResponseAndETAGMixin,
# )
# from rest_framework_extensions.cache.mixins import (
#     CacheResponseMixin,
# )
from . import (
    filters,
    models,
    serializers,
)
from ..base.decorators import docstring_format


@docstring_format(
    model=models.Country.__doc__,
    serializer=serializers.CountrySerializer.__doc__
)
class CountryViewSet(ReadOnlyModelViewSet):
    '''
    List countries.

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
    List languages.

    {model}
    {serializer}
    '''
    queryset = models.Language.objects.all()
    serializer_class = serializers.LanguageSerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.Program.__doc__,
    serializer=serializers.ProgramSerializer.__doc__
)
class ProgramViewSet(ReadOnlyModelViewSet):
    '''
    List programs.

    {model}
    {serializer}
    '''
    queryset = models.Program.objects.all()
    serializer_class = serializers.ProgramSerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.Classification.__doc__,
    serializer=serializers.ClassificationSerializer.__doc__
)
class ClassificationViewSet(ReadOnlyModelViewSet):
    '''
    List OESTAT 2012 classifications.

    {model}
    {serializer}
    '''
    queryset = models.Classification.objects.all()
    serializer_class = serializers.ClassificationSerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.Expertise.__doc__,
    serializer=serializers.ExpertiseSerializer.__doc__
)
class ExpertiseViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List expertise.

    {model}
    {serializer}
    '''
    queryset = models.Expertise.objects.all()
    serializer_class = serializers.ExpertiseSerializer
    permission_classes = (
        AllowAny,
    )
    permit_list_expands = (
        'person',
    )


@docstring_format(
    model=models.Knowledge.__doc__,
    serializer=serializers.KnowledgeSerializer.__doc__
)
class KnowledgeViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List knowledge.

    {model}
    {serializer}
    '''
    queryset = models.Knowledge.objects.all()
    serializer_class = serializers.KnowledgeSerializer
    permission_classes = (
        AllowAny,
    )
    permit_list_expands = (
        'person',
    )


@docstring_format(
    model=models.Education.__doc__,
    serializer=serializers.EducationSerializer.__doc__
)
class EducationViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List educations.

    {model}
    {serializer}
    '''
    queryset = models.Education.objects.all()
    serializer_class = serializers.EducationSerializer
    permission_classes = (
        AllowAny,
    )
    permit_list_expands = (
        'person',
    )


@docstring_format(
    model=models.FunderCategory.__doc__,
    serializer=serializers.FunderCategorySerializer.__doc__
)
class FunderCategoryViewSet(ReadOnlyModelViewSet):
    '''
    List funder categories.

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
    List funders.

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
    List project categories.

    {model}
    {serializer}
    '''
    queryset = models.ProjectCategory.objects.filter(public=True)
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
    List project research.

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
    List project partner functions.

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
    List project studies.

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
    List project events.

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
    List project grants.

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
    List project status.

    {model}
    {serializer}
    '''
    queryset = models.ProjectStatus.objects.filter(public=True)
    serializer_class = serializers.ProjectStatusSerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.Project.__doc__,
    serializer=serializers.ProjectSerializer.__doc__,
    filter=filters.ProjectFilter.__doc__
)
class ProjectViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List projects.

    {model}
    {serializer}
    {filter}
    '''
    queryset = models.Project.objects.filter(
        status__public=True,
        category__public=True
    )
    serializer_class = serializers.ProjectSerializer
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filter_class = filters.ProjectFilter
    ordering_fields = (
        'begin_planned',
        'begin_effective',
        'end_planned',
        'end_effective',
    )
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
        'program',
    )


class ProjectSearchViewSet(HaystackViewSet):
    index_models = [models.Project]
    serializer_class = serializers.ProjectSearchSerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.PublicationAuthorship.__doc__,
    serializer=serializers.PublicationAuthorshipSerializer.__doc__
)
class PublicationAuthorshipViewSet(ReadOnlyModelViewSet):
    '''
    List publication authorships.

    {model}
    {serializer}
    '''
    queryset = models.PublicationAuthorship.objects.all()
    serializer_class = serializers.PublicationAuthorshipSerializer
    permission_classes = (
        AllowAny,
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
    serializer=serializers.PublicationSerializer.__doc__,
    filter=filters.PublicationFilter.__doc__
)
class PublicationViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List publications.

    {model}
    {serializer}
    {filter}
    '''
    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filter_class = filters.PublicationFilter
    ordering_fields = (
        'year',
    )
    permission_classes = (
        AllowAny,
    )
    permit_list_expands = (
        'persons',
        'category',
        'document',
        'status',
        'program',
        'organization_authorship',
    )


class PublicationSearchViewSet(HaystackViewSet):
    index_models = [models.Publication]
    serializer_class = serializers.PublicationSearchSerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.BiddingDeadline.__doc__,
    serializer=serializers.BiddingDeadlineSerializer.__doc__,
    filter=filters.BiddingDeadlineFilter.__doc__
)
class BiddingDeadlineViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List bidding deadlines.

    {model}
    {serializer}
    {filter}
    '''
    queryset = models.BiddingDeadline.objects.all()
    serializer_class = serializers.BiddingDeadlineSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_class = filters.BiddingDeadlineFilter
    permission_classes = (
        AllowAny,
    )
    permit_list_expands = (
        'deadline',
    )


@docstring_format(
    model=models.BiddingEndowment.__doc__,
    serializer=serializers.BiddingEndowmentSerializer.__doc__,
    filter=filters.BiddingEndowmentFilter.__doc__
)
class BiddingEndowmentViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List bidding endowments.

    {model}
    {serializer}
    {filter}
    '''
    queryset = models.BiddingEndowment.objects.all()
    serializer_class = serializers.BiddingEndowmentSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_class = filters.BiddingEndowmentFilter
    permission_classes = (
        AllowAny,
    )
    permit_list_expands = (
        'bidding',
    )


@docstring_format(
    model=models.Bidding.__doc__,
    serializer=serializers.BiddingSerializer.__doc__,
    filter=filters.BiddingFilter.__doc__
)
class BiddingViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List biddings.

    {model}
    {serializer}
    {filter}
    '''
    queryset = models.Bidding.objects.all()
    serializer_class = serializers.BiddingSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_class = filters.BiddingFilter
    permission_classes = (
        AllowAny,
    )
    permit_list_expands = (
        'funders',
        'deadlines',
        'endowments',
    )
