from haystack import indexes

from .models import Room


class RoomIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='co_code')

    def get_model(self):
        return Room

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
