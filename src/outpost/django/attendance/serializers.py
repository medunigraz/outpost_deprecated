from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from . import models
from ..campusonline.serializers import StudentSerializer


class TerminalSerializer(FlexFieldsModelSerializer):

    expandable_fields = {
        'rooms': (
            'outpost.django.campusonline.serializers.RoomSerializer',
            {
                'source': 'rooms',
                'many': True,
            }
        ),
    }

    class Meta:
        model = models.Terminal
        fields = (
            'id',
            'rooms',
            'config',
        )


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
