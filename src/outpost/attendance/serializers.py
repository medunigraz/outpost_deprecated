from rest_framework import serializers

from . import models


class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Terminal


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
