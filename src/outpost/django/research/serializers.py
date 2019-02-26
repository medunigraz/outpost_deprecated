import logging

from drf_haystack.serializers import HaystackSerializer
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.serializers import (
    CharField,
    PrimaryKeyRelatedField,
)

from . import (
    models,
    search_indexes,
)

logger = logging.getLogger(__name__)


class CountrySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Country
        fields = '__all__'


class LanguageSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Language
        fields = '__all__'


class ClassificationSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `persons`

    '''

    class Meta:
        model = models.Classification
        fields = '__all__'

    @property
    def expandable_fields(self):
        person = 'PersonSerializer'
        request = self.context.get('request', None)
        if request:
            if request.user:
                if request.user.is_authenticated():
                    person = 'AuthenticatedPersonSerializer'
        return {
            'persons': (
                f'outpost.django.campusonline.serializers.{person}',
                {
                    'source': 'persons',
                    'many': True
                }
            ),
        }


class ExpertiseSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `person`

    '''

    class Meta:
        model = models.Expertise
        fields = '__all__'

    @property
    def expandable_fields(self):
        person = 'PersonSerializer'
        request = self.context.get('request', None)
        if request:
            if request.user:
                if request.user.is_authenticated():
                    person = 'AuthenticatedPersonSerializer'
        return {
            'person': (
                f'outpost.django.campusonline.serializers.{person}',
                {
                    'source': 'person',
                }
            ),
        }


class KnowledgeSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `person`

    '''

    person = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Knowledge
        fields = '__all__'

    @property
    def expandable_fields(self):
        person = 'PersonSerializer'
        request = self.context.get('request', None)
        if request:
            if request.user:
                if request.user.is_authenticated():
                    person = 'AuthenticatedPersonSerializer'
        return {
            'person': (
                f'outpost.django.campusonline.serializers.{person}',
                {
                    'source': 'person',
                }
            ),
        }


class EducationSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `person`

    '''

    person = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Education
        fields = '__all__'

    @property
    def expandable_fields(self):
        person = 'PersonSerializer'
        request = self.context.get('request', None)
        if request:
            if request.user:
                if request.user.is_authenticated():
                    person = 'AuthenticatedPersonSerializer'
        return {
            'person': (
                f'outpost.django.campusonline.serializers.{person}',
                {
                    'source': 'person',
                }
            ),
        }


class FunderCategorySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.FunderCategory
        fields = '__all__'


class FunderSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `persons`
     * `organizations`
     * `category`
     * `document`

    '''
    class Meta:
        model = models.Funder
        fields = '__all__'

    expandable_fields = {
        'category': (
            FunderCategorySerializer,
            {
                'source': 'category',
            }
        ),
        'country': (
            CountrySerializer,
            {
                'source': 'country',
            }
        ),
    }


class ProjectCategorySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.ProjectCategory
        exclude = (
            'public',
        )


class ProjectResearchSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.ProjectResearch
        fields = '__all__'


class ProjectPartnerFunctionSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.ProjectPartnerFunction
        fields = '__all__'


class ProjectStudySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.ProjectStudy
        fields = '__all__'


class ProjectEventSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.ProjectEvent
        fields = '__all__'


class ProjectGrantSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.ProjectGrant
        fields = '__all__'


class ProjectStatusSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.ProjectStatus
        exclude = (
            'public',
        )


class ProjectSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `organization`
     * `category`
     * `partner_function`
     * `manager`
     * `contact`
     * `status`
     * `grant`
     * `research`
     * `event`
     * `study`
     * `language`
     * `funders`

    '''

    @property
    def expandable_fields(self):
        person = 'PersonSerializer'
        request = self.context.get('request', None)
        if request:
            if request.user:
                if request.user.is_authenticated():
                    person = 'AuthenticatedPersonSerializer'
        return {
            'organization': (
                'outpost.django.campusonline.serializers.OrganizationSerializer',
                {
                    'source': 'organization',
                }
            ),
            'category': (
                ProjectCategorySerializer,
                {
                    'source': 'category',
                }
            ),
            'partner_function': (
                ProjectPartnerFunctionSerializer,
                {
                    'source': 'partner_function',
                }
            ),
            'manager': (
                f'outpost.django.campusonline.serializers.{person}',
                {
                    'source': 'manager',
                }
            ),
            'contact': (
                f'outpost.django.campusonline.serializers.{person}',
                {
                    'source': 'contact',
                }
            ),
            'status': (
                ProjectStatusSerializer,
                {
                    'source': 'status',
                }
            ),
            'grant': (
                ProjectGrantSerializer,
                {
                    'source': 'grant',
                }
            ),
            'research': (
                ProjectResearchSerializer,
                {
                    'source': 'research',
                }
            ),
            'event': (
                ProjectEventSerializer,
                {
                    'source': 'event',
                }
            ),
            'study': (
                ProjectStudySerializer,
                {
                    'source': 'study',
                }
            ),
            'language': (
                LanguageSerializer,
                {
                    'source': 'language',
                }
            ),
            'funders': (
                FunderSerializer,
                {
                    'source': 'funders',
                    'many': True,
                }
            ),
        }

    class Meta:
        model = models.Project
        fields = '__all__'


class ProjectSearchSerializer(HaystackSerializer):
    class Meta:
        index_classes = [search_indexes.ProjectIndex]
        fields = (
            'text',
        )


class PublicationCategorySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.PublicationCategory
        fields = '__all__'


class PublicationDocumentSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.PublicationDocument
        fields = '__all__'


class PublicationSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `persons`
     * `organizations`
     * `category`
     * `document`

    '''
    abstract = CharField(read_only=True)

    @property
    def expandable_fields(self):
        person = 'PersonSerializer'
        request = self.context.get('request', None)
        if request:
            if request.user:
                if request.user.is_authenticated():
                    person = 'AuthenticatedPersonSerializer'
        return {
            'persons': (
                f'outpost.django.campusonline.serializers.{person}',
                {
                    'source': 'persons',
                    'many': True,
                }
            ),
            'organizations': (
                'outpost.django.campusonline.serializers.OrganizationSerializer',
                {
                    'source': 'organizations',
                    'many': True,
                }
            ),
            'category': (
                PublicationCategorySerializer,
                {
                    'source': 'category',
                }
            ),
            'document': (
                PublicationDocumentSerializer,
                {
                    'source': 'document',
                }
            ),
        }

    class Meta:
        model = models.Publication
        exclude = (
            'abstract_bytes',
        )


class PublicationSearchSerializer(HaystackSerializer):
    class Meta:
        index_classes = [search_indexes.PublicationIndex]
        fields = (
            'text',
        )
