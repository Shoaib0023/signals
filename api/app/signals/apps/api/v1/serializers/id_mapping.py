from rest_framework import serializers
from signals.apps.signals.models import IDMapping
from signals.apps.api.generics.serializers import SIAModelSerializer

class IDMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDMapping
        fields = ('id', 'seda_signal_id', 'mb_signal_id', 'facilitator_signal_id', 'mcc_signal_id', 'web_form_id')
        read_only_fields = ('id',)
