import logging

from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.serializers import ModelSerializer

from . import models

logger = logging.getLogger(__name__)


class DoctoralSchoolSerializer(ModelSerializer):
    class Meta:
        model = models.DoctoralSchool
        fields = '__all__'


class DisciplineSerializer(ModelSerializer):

    class Meta:
        model = models.Discipline
        fields = '__all__'


class ThesisSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `doctoralschool`
     * `discipline`
     * `editors`

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
            'doctoralschool': (
                DoctoralSchoolSerializer,
                {
                    'source': 'doctoralschool',
                }
            ),
            'discipline': (
                DisciplineSerializer,
                {
                    'source': 'discipline',
                }
            ),
            'editors': (
                f'outpost.django.campusonline.serializers.{person}',
                {
                    'source': 'editors',
                    'many': True,
                }
            ),
        }

    class Meta:
        model = models.Thesis
        fields = '__all__'
