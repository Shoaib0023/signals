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
    signal = serializers.SerializerMethodField()
    reporter = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    class Meta:
        model = SignalsPlan
        fields = (
            '_display',
            'id',
            'signal',
            'reporter',
            'updated_by',
            'report_days',
            'created_at',
            'updated_at',
            'forman_email',
            'schedule_datetime'
        )

    def get_signal(self, obj):
        # print(obj.signal_id)
        if obj.signal_id:
            return PublicSignalSerializerDetail(
                Signal.objects.get(id=obj.signal_id)
            ).data

        return None

    def get_reporter(self, obj):
        if obj.reporter_id:
            return _NestedReporterModelSerializer(
                Reporter.objects.get(id=obj.reporter_id)
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
    signal_id = serializers.CharField()
    reporter_id = serializers.CharField()
    updated_by = UserDetailHALSerializer(required=False)
    signal = serializers.SerializerMethodField()
    reporter = serializers.SerializerMethodField()

    class Meta:
        model = SignalsPlan
        fields = (
          '_display',
          'id',
          'signal_id',
          'reporter_id',
          'updated_by',
          'updated_at',
          'report_days',
          'created_at',
          'forman_email',
          'schedule_datetime',
          'signal',
          'reporter'
       )

    def get_signal(self, obj):
        if obj.signal_id:
          return PublicSignalSerializerDetail(
              Signal.objects.get(id=obj.signal_id)
          ).data

        return None

    def get_reporter(self, obj):
        if obj.reporter_id:
            return _NestedReporterModelSerializer(
                Reporter.objects.get(id=obj.reporter_id)
            ).data

        return None

    def create(self, validated_data):
        # print(validated_data)
        signal_id = validated_data.pop('signal_id', None)
        reporter_id = validated_data.pop('reporter_id', None)

        signal = Signal.objects.get(id=signal_id)
        reporter = Reporter.objects.get(id=reporter_id)

        instance = super(PrivateSignalsPlanSerializerDetail, self).create(validated_data)

        instance.signal = signal
        instance.reporter = reporter
        instance.save()

        return instance


    def update(self, instance, validated_data):
        signal_id = validated_data.pop('signal_id', None)
        reporter_id = validated_data.pop('reporter_id', None)

        # logged in user
        logged_in_user = self.context['request'].user
        instance = super(PrivateSignalsPlanSerializerDetail, self).update(instance, validated_data)

        instance.updated_by = logged_in_user
        instance.save()
        instance.refresh_from_db()

        return instance
