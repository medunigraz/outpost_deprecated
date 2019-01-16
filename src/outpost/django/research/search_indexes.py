from celery_haystack.indexes import CelerySearchIndex
from haystack import indexes

from .models import (
    Project,
    Publication,
)


class ProjectIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(
        model_attr='title',
        null=True
    )
    organization = indexes.CharField(
        model_attr='organization',
        null=True
    )
    category = indexes.CharField(
        model_attr='category',
        null=True
    )
    short = indexes.CharField(
        model_attr='short',
        null=True
    )
    manager = indexes.CharField(
        model_attr='manager',
        null=True
    )
    contact = indexes.CharField(
        model_attr='contact',
        null=True
    )

    presentation = indexes.CharField(use_template=True)
    autocomplete = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Project

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class PublicationIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(
        model_attr='title',
        null=True
    )
    source = indexes.CharField(
        model_attr='source',
        null=True
    )
    sci = indexes.CharField(
        model_attr='sci',
        null=True
    )

    presentation = indexes.CharField(use_template=True)
    autocomplete = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Publication

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
