from datapunt_api.rest import DisplayField, HALSerializer
from rest_framework import serializers

from signals.apps.signals.models import SignalCityObject, CityObject, Signal
from signals.apps.api.v1.serializers import CityObjectSerializer, PublicSignalSerializerDetail


class SignalCityObjectSerializerList(HALSerializer):
    _display = DisplayField()
    city_obj = serializers.SerializerMethodField()
    signal = serializers.SerializerMethodField()

    class Meta:
        model = SignalCityObject
        fields = (
            '_display',
            'id',
            'complainID',
            'complainIDall',
            'reportCount',
            'is_Orac',
            'city_obj',
            'signal'
        )

    def get_city_obj(self, obj):
        if obj.city_obj_id:
            return CityObjectSerializer(
                CityObject.objects.get(id=obj.city_obj_id)
            ).data

        return None

    def get_signal(self, obj):
        if obj.signal:
            return PublicSignalSerializerDetail(
                Signal.objects.get(id=obj.signal.id)
            ).data

        return None



class SignalCityObjectSerializerDetail(HALSerializer):
    _display = DisplayField()
    signal_id = serializers.CharField()
    city_obj_id = serializers.CharField()
    signal = serializers.SerializerMethodField()
    city_object = serializers.SerializerMethodField()

    class Meta:
        model = SignalCityObject
        fields = (
            '_display',
            'id',
            'signal_id',
            'signal',
            'city_object',
            'city_obj_id',
            'complainID',
            'complainIDall',
            'reportCount',
            'is_Orac'
        )

    def get_city_object(self, obj):
        if obj.city_obj_id:
            return CityObjectSerializer(
                CityObject.objects.get(id=obj.city_obj_id)
            ).data

        return None

    def get_signal(self, obj):
        if obj.signal_id:
            return PublicSignalSerializerDetail(
                Signal.objects.get(id=obj.signal_id)
            ).data

        return None


    def create(self, validated_data):
        signal_id = validated_data.pop('signal_id')
        city_obj_id = validated_data.pop('city_obj_id')
        signal = Signal.objects.get(id=signal_id)
        city_obj = CityObject.objects.get(id=city_obj_id)

        instance = super(SignalCityObjectSerializerDetail, self).create(validated_data)
        instance.signal = signal
        instance.city_obj = city_obj
        instance.save()

        return instance
