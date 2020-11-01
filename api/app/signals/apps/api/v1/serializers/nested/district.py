from datapunt_api.rest import DisplayField, HALSerializer
from rest_framework import serializers

from signals.apps.signals.models import District


class _NestedDistrictSerializer(HALSerializer):
    class Meta:
        model = District
        fields = (
            'id',
            'name',
            'descriptionId',
        )
