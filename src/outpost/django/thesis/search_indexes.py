from celery_haystack.indexes import CelerySearchIndex
from haystack import indexes

from .models import Thesis


class ThesisIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    topic = indexes.CharField(
        model_attr='topic',
        null=True
    )
    description = indexes.CharField(
        model_attr='description',
        null=True
    )
    prerequisites = indexes.CharField(
        model_attr='prerequisites',
        null=True
    )
    goals = indexes.CharField(
        model_attr='goals',
        null=True
    )
    hypothesis = indexes.CharField(
        model_attr='hypothesis',
        null=True
    )
    methods = indexes.CharField(
        model_attr='methods',
        null=True
    )
    discipline = indexes.CharField(
        model_attr='discipline',
        null=True
    )
    doctoralschool = indexes.CharField(
        model_attr='doctoralschool',
        null=True
    )
    editors = indexes.MultiValueField(
        null=True
    )

    def get_model(self):
        return Thesis

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def prepare_editors(self, obj):
        return [editor.pk for editor in obj.editors.all()] or None
