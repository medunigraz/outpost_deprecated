from rest_framework.serializers import ModelSerializer, BooleanField, DecimalField

from . import models


class RecorderSerializer(ModelSerializer):

    class Meta:
        model = models.Recorder


class EpiphanSerializer(ModelSerializer):

    class Meta:
        model = models.Epiphan
        exclude = (
            'username',
            'password',
            'key',
        )


class EpiphanChannelSerializer(ModelSerializer):
    recording = BooleanField()

    class Meta:
        model = models.EpiphanChannel


class EpiphanSourceSerializer(ModelSerializer):
    volume = DecimalField(max_digits=10, decimal_places=7)

    class Meta:
        model = models.EpiphanSource


class RecordingSerializer(ModelSerializer):

    class Meta:
        model = models.Recording


class RecordingAssetSerializer(ModelSerializer):

    class Meta:
        model = models.RecordingAsset


class EventSerializer(ModelSerializer):

    class Meta:
        model = models.Event
