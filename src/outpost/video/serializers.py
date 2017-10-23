from rest_framework.serializers import (
    ModelSerializer,
)

from . import models


class RecorderSerializer(ModelSerializer):

    class Meta:
        model = models.Recorder


class RecordingSerializer(ModelSerializer):

    class Meta:
        model = models.Recording


class RecordingAssetSerializer(ModelSerializer):

    class Meta:
        model = models.RecordingAsset
