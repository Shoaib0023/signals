from rest_framework import serializers
from signals.apps.signals.models import IDMapping
from signals.apps.api.generics.serializers import SIAModelSerializer

class IDMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDMapping
        fields = ('id', 'seda_signal_id', 'mb_signal_id', 'facilitator_signal_id', 'mcc_signal_id', 'web_form_id', 'issue_final_image')
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        # print("Validated Data : ", validated_data)
        # print("Instance : ", instance)

        if "mb_signal_id" in validated_data:
            instance.mb_signal_id = validated_data["mb_signal_id"]
        
        if "issue_final_image" in validated_data:
            instance.issue_final_image = validated_data["issue_final_image"]

        instance.save()
        return instance


