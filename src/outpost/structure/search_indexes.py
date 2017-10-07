from celery_haystack.indexes import CelerySearchIndex
from haystack import indexes

from .models import (
    Organization,
    Person,
)


class OrganizationIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(
        model_attr='campusonline__name',
        null=True
    )
    address = indexes.CharField(
        model_attr='campusonline__address',
        null=True
    )
    level_id = indexes.IntegerField(
        model_attr='office__level__pk',
        null=True
    )
    room_id = indexes.IntegerField(
        model_attr='office__pk',
        null=True
    )
    presentation = indexes.CharField(use_template=True)
    autocomplete = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Organization

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(hidden=False)

    def prepare(self, obj):
        data = super().prepare(obj)
        data['boost'] = 3.0
        return data


class PersonIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    first_name = indexes.CharField(
        model_attr='campusonline__first_name',
        null=True
    )
    last_name = indexes.CharField(
        model_attr='campusonline__last_name',
        null=True
    )
    level_id = indexes.IntegerField(
        model_attr='room__level__pk',
        null=True
    )
    room_id = indexes.IntegerField(
        model_attr='room__pk',
        null=True
    )
    presentation = indexes.CharField(use_template=True)
    autocomplete = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Person

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(hidden=False)

    def prepare(self, obj):
        data = super().prepare(obj)
        data['boost'] = 2.0
        return data
