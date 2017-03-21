from drf_haystack.serializers import HaystackSerializerMixin
from rest_framework.serializers import (
    ModelSerializer,
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
    class Meta:
        model = models.Event
        fields = (
            '__all__'
        )
        exclude = tuple()


class EventSearchSerializer(HaystackSerializerMixin, EventSerializer):
    class Meta(EventSerializer.Meta):
        field_aliases = None
        search_fields = (
            'text',
        )


class NewsSerializer(ModelSerializer):
    class Meta:
        model = models.News
        fields = (
            '__all__'
        )
        exclude = tuple()


class NewsSearchSerializer(HaystackSerializerMixin, NewsSerializer):
    class Meta(NewsSerializer.Meta):
        field_aliases = None
        search_fields = (
            'text',
        )
