from drf_haystack.serializers import HaystackSerializerMixin
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    ReadOnlyField,
    URLField,
)

from . import (
    models,
    search_indexes,
)


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = models.Language
        fields = '__all__'


class GroupSerializer(ModelSerializer):

    class Meta:
        model = models.Group
        fields = '__all__'


class CategorySerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `language`

    '''
    expandable_fields = {
        'language': (
            'outpost.typo3.serializers.LanguageSerializer',
            {
                'source': 'language',
            }
        ),
    }

    class Meta:
        model = models.Category
        exclude = (
            'marker',
        )


class CalendarSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `language`

    '''
    expandable_fields = {
        'language': (
            'outpost.typo3.serializers.LanguageSerializer',
            {
                'source': 'language',
            }
        ),
    }

    class Meta:
        model = models.Calendar
        fields = '__all__'


class EventMediaSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `language`

    '''
    expandable_fields = {
        'language': (
            'outpost.typo3.serializers.LanguageSerializer',
            {
                'source': 'language',
            }
        ),
    }

    class Meta:
        model = models.EventMedia
        fields = '__all__'


class EventCategorySerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `calendar`
     * `language`

    '''
    expandable_fields = {
        'calendar': (
            'outpost.typo3.serializers.CalendarSerializer',
            {
                'source': 'calendar',
            }
        ),
        'language': (
            'outpost.typo3.serializers.LanguageSerializer',
            {
                'source': 'language',
            }
        ),
    }

    class Meta:
        model = models.EventCategory
        fields = '__all__'


class EventSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `calendar`
     * `language`

    '''
    expandable_fields = {
        'calendar': (
            'outpost.typo3.serializers.CalendarSerializer',
            {
                'source': 'calendar',
            }
        ),
        'language': (
            'outpost.typo3.serializers.LanguageSerializer',
            {
                'source': 'language',
            }
        ),
    }
    media = EventMediaSerializer(many=True, read_only=True)
    breadcrumb = ReadOnlyField()
    url = URLField(read_only=True, allow_null=True)

    class Meta:
        model = models.Event
        exclude = (
            'page',
        )


class EventSearchSerializer(HaystackSerializerMixin, EventSerializer):
    url = URLField(read_only=True, allow_null=True)

    class Meta(EventSerializer.Meta):
        field_aliases = None
        search_fields = (
            'text',
        )


class NewsMediaSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `language`

    '''
    expandable_fields = {
        'language': (
            'outpost.typo3.serializers.LanguageSerializer',
            {
                'source': 'language',
            }
        ),
    }

    class Meta:
        model = models.NewsMedia
        fields = '__all__'


class NewsSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `categories`
     * `language`

    '''
    expandable_fields = {
        'categories': (
            'outpost.typo3.serializers.CategorySerializer',
            {
                'source': 'categories',
                'many': True,
            }
        ),
        'language': (
            'outpost.typo3.serializers.LanguageSerializer',
            {
                'source': 'language',
            }
        ),
    }
    url = URLField(read_only=True, allow_null=True)
    media = NewsMediaSerializer(many=True, read_only=True)
    breadcrumb = ReadOnlyField()
    categories = PrimaryKeyRelatedField(many=True, read_only=True)
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = models.News
        exclude = (
            'page',
            'tags',
        )


class NewsSearchSerializer(HaystackSerializerMixin, NewsSerializer):
    url = URLField(read_only=True, allow_null=True)

    class Meta(NewsSerializer.Meta):
        field_aliases = None
        search_fields = (
            'text',
        )
