from rest_framework import (
    permissions,
    viewsets,
)

from . import (
    models,
    serializers,
)


class TokenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Token.objects.all()
    serializer_class = serializers.TokenSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
