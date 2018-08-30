from drf_haystack.serializers import HaystackSerializerMixin
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


class CategorySerializer(ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class CalendarSerializer(ModelSerializer):
    class Meta:
        model = models.Calendar
        fields = '__all__'


class EventMediaSerializer(ModelSerializer):

    class Meta:
        model = models.EventMedia
        fields = '__all__'


class EventSerializer(ModelSerializer):
    media = EventMediaSerializer(many=True, read_only=True)
    url = URLField(read_only=True, allow_null=True)

    class Meta:
        model = models.Event
        fields = '__all__'


class EventSearchSerializer(HaystackSerializerMixin, EventSerializer):
    url = URLField(read_only=True, allow_null=True)

    class Meta(EventSerializer.Meta):
        field_aliases = None
        search_fields = (
            'text',
        )
        fields = '__all__'


class NewsCategorySerializer(ModelSerializer):

    class Meta:
        model = models.NewsCategory
        fields = (
            'category',
        )


class NewsMediaSerializer(ModelSerializer):

    class Meta:
        model = models.NewsMedia
        fields = '__all__'


class NewsSerializer(ModelSerializer):
    url = URLField(read_only=True, allow_null=True)
    categories = PrimaryKeyRelatedField(many=True, read_only=True)
    media = NewsMediaSerializer(many=True, read_only=True)
    breadcrumb = ReadOnlyField()

    class Meta:
        model = models.News
        fields = '__all__'


class NewsSearchSerializer(HaystackSerializerMixin, NewsSerializer):
    url = URLField(read_only=True, allow_null=True)

    class Meta(NewsSerializer.Meta):
        field_aliases = None
        search_fields = (
            'text',
        )
        fields = '__all__'
