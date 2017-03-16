from drf_haystack.serializers import HaystackSerializer
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


class NewsSerializer(ModelSerializer):
    class Meta:
        model = models.News


class NewsSearchSerializer(HaystackSerializer):
    class Meta:
        index_classes = [search_indexes.NewsIndex]
        fields = [
            'text',
        ]
