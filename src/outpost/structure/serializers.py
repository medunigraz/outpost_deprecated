from rest_framework.serializers import ModelSerializer

from ..campusonline import serializers as campusonline
from ..geo import serializers as geo
from . import models


class OrganizationSerializer(ModelSerializer):
    campusonline = campusonline.OrganizationSerializer(
        many=False,
        read_only=True
    )
    office = geo.RoomSerializer(
        many=False,
        read_only=True
    )

    class Meta:
        model = models.Organization
        exclude = (
            'hidden',
        )


class PersonSerializer(ModelSerializer):
    campusonline = campusonline.PersonSerializer(
        many=False,
        read_only=True
    )
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
