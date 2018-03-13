from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_gis.filters import DistanceToPointFilter

from apps.location.models import Location
from apps.location.serializers import LocationSerializer


class LocationListView(generics.ListCreateAPIView):
    """
    get:
        Get list of locations.

    post:
        Create new Location.
    """
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    filter_backends = (DistanceToPointFilter, DjangoFilterBackend, OrderingFilter, SearchFilter)
    distance_filter_field = 'point'
    filter_fields = ('id', 'user', 'zipcode', 'country')
    ordering_fields = ('id', 'user', 'street', 'city', 'state', 'zipcode', 'country')
    search_fields = (
        'id', 'user__username', 'user__email', 'user__first_name', 'user__last_name', 'street', 'city', 'state',
        'country'
    )
    ordering = ('user',)


class LocationDetailView(generics.RetrieveUpdateAPIView):
    """
    get:
        Get location details.

    put:
        Update Location.

    patch:
        Update Location.
    """
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
