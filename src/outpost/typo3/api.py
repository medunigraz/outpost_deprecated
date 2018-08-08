from django.utils import timezone
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

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


class LanguageViewSet(ReadOnlyModelViewSet):
    queryset = models.Language.objects.all()
    serializer_class = serializers.LanguageSerializer
    permission_classes = (
        AllowAny,
    )
    filter_fields = (
        'isocode',
    )


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (
        AllowAny,
    )
    filter_fields = (
        'language',
        'start',
        'end',
    )


class CalendarViewSet(ReadOnlyModelViewSet):
    queryset = models.Calendar.objects.all()
    serializer_class = serializers.CalendarSerializer
    permission_classes = (
        AllowAny,
    )
    filter_fields = (
        'language',
    )


class EventViewSet(ReadOnlyModelViewSet):
    queryset = models.Event.objects.filter(end__gte=timezone.now())
    serializer_class = serializers.EventSerializer
    permission_classes = (
        AllowAny,
    )
    filter_fields = (
        'start',
        'end',
        'allday',
        'location',
        'register',
        'registration_end',
        'attending_fees',
        'dfp_points',
        'target',
        'calendar',
        'category',
        'language',
    )


class EventSearchViewSet(HaystackViewSet):
    index_models = [models.Event]
    serializer_class = serializers.EventSearchSerializer
    permission_classes = (
        AllowAny,
    )


class NewsViewSet(ReadOnlyModelViewSet):
    queryset = models.News.objects.all()
    serializer_class = serializers.NewsSerializer
    permission_classes = (
        AllowAny,
    )
    filter_fields = (
        'page',
        'topnews',
        'email',
        'language',
    )


class NewsSearchViewSet(HaystackViewSet):
    index_models = [models.News]
    serializer_class = serializers.NewsSearchSerializer
    permission_classes = (
        AllowAny,
    )
