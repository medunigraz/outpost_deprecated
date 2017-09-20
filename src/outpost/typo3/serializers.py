from drf_haystack.serializers import HaystackSerializerMixin
from rest_framework.serializers import (
    ModelSerializer,
    URLField,
)

from . import (
    models,
    search_indexes,
)


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = models.Language


class CategorySerializer(ModelSerializer):
    class Meta:
        model = models.Category


class CalendarSerializer(ModelSerializer):
    class Meta:
        model = models.Calendar


class EventSerializer(ModelSerializer):
    url = URLField(read_only=True, allow_null=True)

    class Meta:
        model = models.Event
        fields = (
            '__all__'
        )
        exclude = tuple()


class EventSearchSerializer(HaystackSerializerMixin, EventSerializer):
    url = URLField(read_only=True, allow_null=True)

    class Meta(EventSerializer.Meta):
        field_aliases = None
        search_fields = (
            'text',
        )


class NewsSerializer(ModelSerializer):
    url = URLField(read_only=True, allow_null=True)

    class Meta:
        model = models.News
        fields = (
            '__all__'
        )
        exclude = tuple()


class NewsSearchSerializer(HaystackSerializerMixin, NewsSerializer):
    url = URLField(read_only=True, allow_null=True)

    class Meta(NewsSerializer.Meta):
        field_aliases = None
        search_fields = (
            'text',
        )
