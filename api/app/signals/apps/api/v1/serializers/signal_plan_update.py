from datapunt_api.rest import DisplayField, HALSerializer
from rest_framework import serializers

from signals.apps.signals.models import SignalPlanUpdate, Signal

class SignalPlanUpdateSerializer(HALSerializer):
    class Meta:
        model = SignalPlanUpdate
        fields = (
            'signal_id',
            'description',
            'assign_to',
            'image',
            'created_at',
            'updated_at',
            )
            
        extra_kwargs = {
            'signal_id': {'write_only': True}
        }

        read_only_fields = (
            'created_at',
            'updated_at'
        )

    def create(self, validated_data):
        signal_id = validated_data.get('signal_id')
        signal = Signal.objects.get(signal_id=signal_id)

        instance = super(SignalPlanUpdateSerializer, self).create(validated_data)
        signal.updates.add(instance)
        return instance 
