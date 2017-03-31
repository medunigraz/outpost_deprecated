from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex

from .models import News, Event


class NewsIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True
    )
    language = indexes.FacetCharField(
        model_attr='language__title'
    )
    start = indexes.DateTimeField(
        model_attr='start',
        null=True
    )
    end = indexes.DateTimeField(
        model_attr='end',
        null=True
    )
    topnews = indexes.FacetBooleanField(
        model_attr='topnews'
    )

    def get_model(self):
        return News

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class EventIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True
    )
    language = indexes.FacetCharField(
        model_attr='language__title'
    )
    category = indexes.FacetCharField(
        model_attr='category__title'
    )
    start = indexes.DateTimeField(
        model_attr='start',
        null=True
    )
    end = indexes.DateTimeField(
        model_attr='end',
        null=True
    )
    allday = indexes.FacetBooleanField(
        model_attr='allday'
    )
    register = indexes.FacetBooleanField(
        model_attr='register'
    )
    attending_fees = indexes.FacetBooleanField(
        model_attr='attending_fees'
    )

    def get_model(self):
        return Event

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
