from datapunt_api.rest import DisplayField, HALSerializer
from rest_framework import serializers

from signals.apps.signals.models import District, Neighbourhood, PostCode
from signals.apps.api.v1.serializers.neighbourhood import NeighbourhoodSerializer
from signals.apps.api.v1.serializers.nested.district import _NestedDistrictSerializer

class PostCodeSerializer(HALSerializer):
    district_id = serializers.CharField(required=False)
    neigh_id = serializers.CharField(required=False)
    # district = serializers.SerializerMethodField(required=False)
    neighbourhood = serializers.SerializerMethodField(required=False)

    class Meta:
        model = PostCode
        fields = (
            'post_code',
            'district_id',
            'neigh_id',
            'neighbourhood',
        )
        extra_kwargs = {
            'district_id': {"write_only": "True"},
            'neigh_id': {"write_only": "True"}
        }

    # def get_district(self, obj):
    #     if obj.stadsdeelId:
    #         return _NestedDistrictSerializer(
    #             District.objects.get(id=obj.stadsdeelId.id)
    #         ).data

    #     return None

    def get_neighbourhood(self, obj):
        if obj.neighbourhood:
            return NeighbourhoodSerializer(
                Neighbourhood.objects.get(id=obj.neighbourhood.id)
            ).data

        return None
    
    def create(self, validated_data):         
        print("Validated_data", validated_data)
        district_id = validated_data.pop('district_id', None)
        neigh_id = validated_data.pop('neigh_id', None)

        if district_id:
            district = District.objects.get(id=district_id)

        if neigh_id:
            neighbourhood = Neighbourhood.objects.get(id=neigh_id)

        instance = super(PostCodeSerializer, self).create(validated_data)

        if neigh_id:
            instance.neighbourhood = neighbourhood
        instance.save()

        return instance
        
