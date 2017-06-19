from django.urls import reverse_lazy as reverse
from drf_haystack.serializers import HaystackSerializer
from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    SerializerMethodField,
)
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from . import (
    models,
)
from ..campusonline import serializers as campusonline


class BeaconSerializer(GeoFeatureModelSerializer):
    id = SerializerMethodField()

    class Meta:
        model = models.Beacon
        geo_field = 'position'
        id_field = 'id'

    def get_id(self, obj):
        return str(obj.mac)
