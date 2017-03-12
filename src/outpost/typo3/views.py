from drf_haystack.viewsets import HaystackViewSet
from rest_framework.filters import DjangoFilterBackend
from rest_framework.viewsets import (
    ReadOnlyModelViewSet,
)
# from rest_framework_extensions.mixins import (
#     CacheResponseAndETAGMixin,
# )
# from rest_framework_extensions.cache.mixins import (
#     CacheResponseMixin,
# )
from . import (
    models,
    serializers,
)


class NewsViewSet(ReadOnlyModelViewSet):
    queryset = models.News.objects.all()
    serializer_class = serializers.NewsSerializer


class NewsSearchViewSet(HaystackViewSet):
    index_models = [models.News]
    serializer_class = serializers.NewsSearchSerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
