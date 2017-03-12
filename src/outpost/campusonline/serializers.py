from rest_framework.serializers import (
    ModelSerializer,
)

from . import (
    models,
)


class RoomSerializer(ModelSerializer):
    class Meta:
        model = models.Room


class FloorSerializer(ModelSerializer):
    class Meta:
        model = models.Floor


class BuildingSerializer(ModelSerializer):
    class Meta:
        model = models.Building
