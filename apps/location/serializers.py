from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from apps.location.models import Location


class LocationSerializer(GeoFeatureModelSerializer):
    """
    List Serializer for Location model.
    """
    class Meta:
        model = Location
        fields = '__all__'
        geo_field = 'point'
