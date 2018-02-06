from rest_framework import serializers

from . import models


class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Terminal
        fields = '__all__'


class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Holding
        fields = '__all__'


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Entry
        fields = '__all__'
