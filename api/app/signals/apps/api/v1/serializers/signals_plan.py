from datapunt_api.rest import DisplayField, HALSerializer
from rest_framework import serializers

from signals.apps.signals.models.signal import Signal
from signals.apps.signals.models.reporter import Reporter
from signals.apps.signals.models.signals_plan import SignalsPlan
from signals.apps.api.v1.serializers.nested.reporter import _NestedReporterModelSerializer
from signals.apps.api.v1.serializers.signal import PublicSignalSerializerDetail, PrivateSignalSerializerDetail, PrivateSignalSerializerList

from django.contrib.auth.models import User
from signals.apps.users.v1.serializers import UserListHALSerializer, UserDetailHALSerializer

class PrivateSignalsPlanSerializerList(HALSerializer):
    _display = DisplayField()
    report = serializers.SerializerMethodField()
    emp = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    class Meta:
        model = SignalsPlan
        fields = (
            '_display',
            'id',
            'signal',
            'emp',
            'updated_by',
            'report_days',
            'created_at',
            'updated_at',
            'forman_email',
            'schedule'
        )

    def get_signal(self, obj):
        # print(obj.report)
        if obj.signal and obj.signal.id:
            return PublicSignalSerializerDetail(
                Signal.objects.get(signal_id=obj.signal.signal_id)
            ).data

        return None

    def get_emp(self, obj):
        if obj.emp and obj.emp.id:
            return _NestedReporterModelSerializer(
                Reporter.objects.get(id=obj.emp.id)
            ).data

        return None

    def get_updated_by(self, obj):
        if obj.updated_by and obj.updated_by.email:
            return UserListHALSerializer(
                User.objects.get(email=obj.updated_by.email)
            ).data

        return None


class PrivateSignalsPlanSerializerDetail(HALSerializer):
    _display = DisplayField()
    signal = PublicSignalSerializerDetail()
    emp =  _NestedReporterModelSerializer()
    updated_by = UserDetailHALSerializer(required=False)

    class Meta:
        model = SignalsPlan
        fields = (
          '_display',
          'signal',
          'emp',
          'updated_by',
          'updated_at',
          'report_days',
          'created_at',
          'forman_email',
          'schedule'
       )

    def create(self, validated_data):
        signal_data = validated_data.pop('signal', None)
        emp_data = validated_data.pop('emp', None)

        signal = Signal.objects.get(signal_id=signal_data["signal_id"])
        emp = Reporter.objects.get(id=emp_data["id"])

        instance = super(PrivateSignalsPlanSerializerDetail, self).create(validated_data)

        instance.signal = signal
        instance.emp = emp
        instance.save()

        return instance


    def update(self, instance, validated_data):
        signal_data = validated_data.pop('signal', None)
        emp_data = validated_data.pop('emp', None)

        # logged in user
        logged_in_user = self.context['request'].user

        instance = super(PrivateSignalsPlanSerializerDetail, self).update(instance, validated_data)
        instance.updated_by = logged_in_user
        instance.save()
        instance.refresh_from_db()
        
        return instance
