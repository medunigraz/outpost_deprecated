from rest_framework.utils.mediatypes import (
    media_type_matches,
    order_by_precedence,
)
from rest_framework.viewsets import ModelViewSet
from reversion.views import RevisionMixin


class MediatypeNegotiationMixin(object):

    def get_serializer_class(self):
        classes = getattr(self, 'mediatype_serializer_classes', None)
        serializer = None
        if isinstance(classes, dict):
            if self.request.method.lower() not in ('GET', 'HEAD', 'OPTIONS'):
                serializer = classes.get(self.request.content_type, None)
            else:
                header = self.request.META.get('HTTP_ACCEPT', '*/*')
                tokens = [token.strip() for token in header.split(',')]
                for a in order_by_precedence(tokens):
                    serializer = next((c for (k, c) in classes if media_type_matches(k, a)), None)
        if serializer:
            return serializer
        return super(MediatypeNegotiationMixin, self).get_serializer_class()


class GeoModelViewSet(MediatypeNegotiationMixin, RevisionMixin, ModelViewSet):
    pass
