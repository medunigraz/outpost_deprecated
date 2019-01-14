import logging

from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from . import models

logger = logging.getLogger(__name__)


class CategorySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class DocumentSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Document
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
    abstract = serializers.CharField(read_only=True)

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
                f'outpost.campusonline.serializers.{person}',
                {
                    'source': 'persons',
                    'many': True,
                }
            ),
            'organizations': (
                'outpost.campusonline.serializers.OrganzationSerializer',
                {
                    'source': 'organizations',
                    'many': True,
                }
            ),
            'category': (
                CategorySerializer,
                {
                    'source': 'category',
                }
            ),
            'document': (
                DocumentSerializer,
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
