from rest_framework import serializers

from . import models


class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Terminal


class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Holding


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Entry
