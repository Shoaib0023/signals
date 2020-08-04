from rest_framework import serializers
from signals.apps.signals.models import City
from signals.apps.api.generics.serializers import SIAModelSerializer

class CitySerializer(SIAModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'city_name',)
        read_only_fields = ('id',)
