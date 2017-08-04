from rest_framework.serializers import ModelSerializer

from . import models
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

    class Meta:
        model = models.Organization
        exclude = (
            'hidden',
        )


class PersonSerializer(ModelSerializer):
    campusonline = campusonline.PersonNameSerializer(
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
