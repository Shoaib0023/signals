from rest_framework import serializers
from signals.apps.signals.models import Country
from signals.apps.api.generics.serializers import SIAModelSerializer

class CountrySerializer(SIAModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'country_name',)
        read_only_fields = ('id',)
