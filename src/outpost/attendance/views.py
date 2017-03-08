from rest_framework import viewsets

from . import (
    models,
    serializers,
)


class HoldingViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = models.Holding.objects.all()
    serializer_class = serializers.HoldingSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer


class EntryViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = models.Entry.objects.all()
    serializer_class = serializers.EntrySerializer
