from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

from . import models
from ..base.utils import colorscale
from ..campusonline import serializers as campusonline
from ..geo import serializers as geo


class OrganizationSerializer(ModelSerializer):
    campusonline = campusonline.OrganizationSerializer(
        many=False,
        read_only=True
    )
    office = geo.RoomSerializer(
        many=False,
        read_only=True
    )
    color = SerializerMethodField()

    class Meta:
        model = models.Organization
        exclude = (
            'hidden',
        )

    def get_color(self, obj):
        return {
            'base': obj.color,
            'lighter': colorscale(obj.color, 1.2),
            'darker': colorscale(obj.color, 0.8),
        }


class PersonSerializer(ModelSerializer):
    # campusonline = campusonline.PersonNameSerializer(
    #     many=False,
    #     read_only=True
    # )
    room = geo.RoomSerializer(
        many=False,
        read_only=True
    )

    class Meta:
        model = models.Person
        exclude = (
            'hidden',
            'campusonline',
        )
