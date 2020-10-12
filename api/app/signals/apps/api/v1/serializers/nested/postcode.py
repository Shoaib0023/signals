from datapunt_api.rest import DisplayField, HALSerializer
from rest_framework import serializers

from signals.apps.signals.models import PostCode
from signals.apps.api.v1.serializers.nested.district import _NestedDistrictSerializer


class _NestedPostCodeSerializer(HALSerializer):
    stadsdeel = _NestedDistrictSerializer(
                source = 'stadsdeelId'
            )

    class Meta:
        model = PostCode
        fields = (
            'post_code',
            'stadsdeel',
        )
