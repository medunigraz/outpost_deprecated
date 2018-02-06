from rest_framework import serializers

from outpost.api.serializers import Base64FileField
from outpost.geo.serializers import RoomSerializer
from . import models


class ExportClassSerializer(serializers.BaseSerializer):
    id = serializers.CharField(max_length=256)
    name = serializers.CharField(max_length=256)

    def to_representation(self, cls):
        return {
            'id': cls[0],
            'name': cls[1],
        }


class RecorderSerializer(serializers.ModelSerializer):
    room = RoomSerializer()

    class Meta:
        model = models.Recorder
        fields = '__all__'


class EpiphanSerializer(RecorderSerializer):

    class Meta:
        model = models.Epiphan
        exclude = (
            'username',
            'password',
            'key',
        )


class EpiphanChannelSerializer(serializers.ModelSerializer):
    recording = serializers.BooleanField()

    class Meta:
        model = models.EpiphanChannel
        fields = '__all__'


class EpiphanSourceSerializer(serializers.ModelSerializer):
    volume = serializers.DecimalField(max_digits=10, decimal_places=7)

    class Meta:
        model = models.EpiphanSource
        fields = '__all__'


class RecordingSerializer(serializers.ModelSerializer):
    recorder = RecorderSerializer()

    class Meta:
        model = models.Recording
        fields = '__all__'


class RecordingAssetSerializer(serializers.ModelSerializer):
    data = Base64FileField()

    class Meta:
        model = models.RecordingAsset
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Event
        fields = '__all__'


class DASHPublishSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DASHPublish
        fields = '__all__'


class DASHAudioSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DASHAudio
        fields = '__all__'


class DASHVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DASHVideo
        fields = '__all__'


class DASHVideoVariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DASHVideoVariant
        fields = '__all__'
