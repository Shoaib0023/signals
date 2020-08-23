from datapunt_api.rest import DisplayField, HALSerializer
from rest_framework import serializers

from signals.apps.signals.models import CityObject

class CityObjectSerializer(HALSerializer):
    class Meta:
        model = CityObject
        fields = (
            'id',
            'oracCode',
            'orac_comment',
            'oracCategory',
            'oracType'
        )

    def create(self, validated_data):
        oracCode = validated_data.get('oraccode')
        orac_comment = validated_data.get('orac_commment', None)
        oracCategory = validated_data.get('oracCategory')
        oracType = validated_data.get('oracType', None)

        instance = super(CityObjectSerializer, self).create(validated_data)
        instance.refresh_from_db()
        return instance
