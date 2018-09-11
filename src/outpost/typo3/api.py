from django.utils import timezone
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from outpost.base.decorators import docstring_format

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


@docstring_format(model=models.Language.__doc__)
class LanguageViewSet(ReadOnlyModelViewSet):
    '''
    List languages from TYPO3.

    {model}
    '''
    queryset = models.Language.objects.all()
    serializer_class = serializers.LanguageSerializer
    permission_classes = (
        AllowAny,
    )
    filter_fields = (
        'isocode',
    )


@docstring_format(model=models.Category.__doc__)
class CategoryViewSet(ReadOnlyModelViewSet):
    '''
    List categories from TYPO3.

    {model}
    '''
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


@docstring_format(model=models.Calendar.__doc__)
class CalendarViewSet(ReadOnlyModelViewSet):
    '''
    List calendars from TYPO3.

    {model}
    '''
    queryset = models.Calendar.objects.all()
    serializer_class = serializers.CalendarSerializer
    permission_classes = (
        AllowAny,
    )
    filter_fields = (
        'language',
    )


@docstring_format(model=models.EventCategory.__doc__)
class EventCategoryViewSet(ReadOnlyModelViewSet):
    '''
    List event categories from TYPO3.

    {model}
    '''
    queryset = models.EventCategory.objects.all()
    serializer_class = serializers.EventCategorySerializer
    permission_classes = (
        AllowAny,
    )
    filter_fields = (
        'calendar',
        'language',
    )


@docstring_format(model=models.Event.__doc__)
class EventViewSet(ReadOnlyModelViewSet):
    '''
    List events from TYPO3.

    {model}
    '''
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
        'calendar',
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
