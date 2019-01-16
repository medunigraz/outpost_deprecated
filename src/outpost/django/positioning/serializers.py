from rest_framework_gis.serializers import GeoFeatureModelSerializer

from . import models


class BeaconSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = models.Beacon
        geo_field = 'position'
        fields = '__all__'
