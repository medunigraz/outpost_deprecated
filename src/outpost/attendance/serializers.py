from datetime import timedelta

from rest_framework import serializers

from . import models
from ..api import validators


class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Holding


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Entry
        fields = ['id', 'student', 'direction']
        validators = [
            validators.EntryThrottleValidator(
                models.Entry.objects.all(),
                'student',
                'time',
                timedelta(seconds=60)
            )
        ]
