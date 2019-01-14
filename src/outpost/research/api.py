from rest_flex_fields.views import FlexFieldsMixin
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


@docstring_format(
    model=models.Category.__doc__,
    serializer=serializers.CategorySerializer.__doc__
)
class CategoryViewSet(ReadOnlyModelViewSet):
    '''
    List publication categories.

    {model}
    {serializer}
    '''
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.Document.__doc__,
    serializer=serializers.DocumentSerializer.__doc__
)
class DocumentViewSet(ReadOnlyModelViewSet):
    '''
    List publication documents.

    {model}
    {serializer}
    '''
    queryset = models.Document.objects.all()
    serializer_class = serializers.DocumentSerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.Publication.__doc__,
    serializer=serializers.PublicationSerializer.__doc__
)
class PublicationViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List thesis.

    {model}
    {serializer}
    '''
    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer
    permission_classes = (
        AllowAny,
    )
    permit_list_expands = (
        'persons',
        'organizations',
        'category',
        'document',
    )
