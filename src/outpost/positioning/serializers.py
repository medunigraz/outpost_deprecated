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

    class Meta:
        model = models.Beacon
        geo_field = 'position'
