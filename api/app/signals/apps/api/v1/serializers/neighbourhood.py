from datapunt_api.rest import DisplayField, HALSerializer
from rest_framework import serializers

from signals.apps.signals.models import Neighbourhood, District
from signals.apps.api.v1.serializers.nested.district import _NestedDistrictSerializer


class NeighbourhoodSerializer(HALSerializer):
    district = _NestedDistrictSerializer(required=False)
    district_id = serializers.CharField(required=True)

    class Meta:
        model = Neighbourhood
        fields = (
            'id',
            'name',
            'district',
            'district_id',
        )
        extra_kwargs = {
            'district_id': {"write_only": True}
        }
    
    def create(self, validated_data):         
        print("Validated_data", validated_data)
        district_id = validated_data.pop('district_id', None)
        if district_id:
            district = District.objects.get(id=district_id)

        instance = super(NeighbourhoodSerializer, self).create(validated_data)
        if district_id:
            instance.district = district

        instance.save()

        return instance 