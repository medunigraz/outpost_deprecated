from celery_haystack.indexes import CelerySearchIndex
from haystack import indexes

from .models import BulletinPage


class BulletinPageIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    issue = indexes.CharField(
        model_attr='bulletin__issue',
    )
    academic_year = indexes.CharField(
        model_attr='bulletin__academic_year',
    )

    def get_model(self):
        return BulletinPage

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
