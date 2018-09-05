from rest_framework import serializers

from . import models


class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Terminal
        fields = '__all__'


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Entry
        fields = (
            'terminal',
            'created',
        )


class CampusOnlineHoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CampusOnlineHolding
        fields = '__all__'


class StatisticsEntrySerializer(serializers.ModelSerializer):
    incoming = EntrySerializer(read_only=True)
    outgoing = EntrySerializer(read_only=True)

    class Meta:
        model = models.StatisticsEntry
        fields = (
            'incoming',
            'outgoing',
        )


class StatisticsSerializer(serializers.ModelSerializer):
    entries = StatisticsEntrySerializer(many=True, read_only=True)

    class Meta:
        model = models.Statistics
        fields = (
            'name',
            'entries',
        )
