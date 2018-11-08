import logging

from rest_flex_fields import FlexFieldsModelSerializer

from . import models

logger = logging.getLogger(__name__)


class PublicationSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `person`

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
            'person': (
                f'outpost.campusonline.serializers.{person}',
                {
                    'source': 'person',
                }
            ),
        }

    class Meta:
        model = models.Publication
        fields = '__all__'
