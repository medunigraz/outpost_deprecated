from celery_haystack.indexes import CelerySearchIndex
from haystack import indexes

from .models import Room


class RoomIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(
        model_attr='name',
        null=True
    )
    category = indexes.CharField(
        model_attr='category__name',
        null=True
    )
    organization = indexes.CharField(
        model_attr='campusonline__organization',
        null=True
    )
    building = indexes.CharField(
        model_attr='campusonline__building__name',
        null=True
    )
    address = indexes.CharField(
        model_attr='campusonline__building__address',
        null=True
    )
    campusonline_title = indexes.CharField(
        model_attr='campusonline__title',
        null=True
    )
    campusonline_id = indexes.CharField(
        model_attr='campusonline__name_full',
        null=True
    )
    level_id = indexes.IntegerField(
        model_attr='level__pk',
        null=True
    )
    room_id = indexes.IntegerField(
        model_attr='pk',
        null=True
    )

    presentation = indexes.CharField(use_template=True)
    autocomplete = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Room

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(virtual=False)
