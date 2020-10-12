import os

from datapunt_api.rest import DisplayField, HALSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_gis.fields import GeometryField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from signals.apps.api.generics.permissions import (
    SIAPermissions,
    SignalChangeCategoryPermission,
    SignalChangeStatusPermission,
    SignalCreateInitialPermission,
    SignalCreateNotePermission
)
from signals.apps.api.generics.validators import SignalSourceValidator
from signals.apps.api.v1.fields import (
    PrivateSignalLinksField,
    PrivateSignalLinksFieldWithArchives,
    PublicSignalLinksField
)
from signals.apps.api.v1.fields.extra_properties import SignalExtraPropertiesField
from signals.apps.api.v1.serializers.nested import (
    _NestedCategoryModelSerializer,
    _NestedDepartmentModelSerializer,
    _NestedLocationModelSerializer,
    _NestedNoteModelSerializer,
    _NestedPriorityModelSerializer,
    _NestedPublicStatusModelSerializer,
    _NestedReporterModelSerializer,
    _NestedStatusModelSerializer,
    _NestedTypeModelSerializer
)
from signals.apps.api.v1.validation.address.mixin import AddressValidationMixin
from signals.apps.api.v1.validators.extra_properties import ExtraPropertiesValidator
from signals.apps.signals import workflow
from signals.apps.signals.models import Priority, Signal


from signals.apps.api.v1.serializers.country import CountrySerializer
from signals.apps.api.v1.serializers.city import CitySerializer
from signals.apps.api.v1.serializers.city_object import CityObjectSerializer
from signals.apps.api.v1.serializers.id_mapping import IDMappingSerializer
from signals.apps.api.v1.serializers.signal_plan_update import SignalPlanUpdateSerializer

from signals.apps.signals.models.country import Country
from signals.apps.signals.models.city import City



class PrivateSignalSerializerDetail(HALSerializer, AddressValidationMixin):
    """
    This serializer is used for the detail endpoint and when updating the instance
    """
    serializer_url_field = PrivateSignalLinksFieldWithArchives
    _display = DisplayField()


    country = CountrySerializer(
        required=False,
        permission_classes=(SIAPermissions,)
        )

    city = CitySerializer(
        required=False,
        permission_classes=(SIAPermissions,)
    )

    city_object = CityObjectSerializer(
        many=True,
        required=False
    )

    location = _NestedLocationModelSerializer(
        required=False,
        permission_classes=(SIAPermissions,)
    )

    status = _NestedStatusModelSerializer(
        required=False,
        permission_classes=(SignalChangeStatusPermission,)
    )

    category = _NestedCategoryModelSerializer(
        source='category_assignment',
        required=False,
        permission_classes=(SignalChangeCategoryPermission,)
    )

    reporter = _NestedReporterModelSerializer(
        required=False,
        permission_classes=(SIAPermissions,)
    )

    priority = _NestedPriorityModelSerializer(
        required=False,
        permission_classes=(SIAPermissions,)
    )

    notes = _NestedNoteModelSerializer(
        many=True,
        required=False,
        permission_classes=(SignalCreateNotePermission,)
    )

    type = _NestedTypeModelSerializer(
        required=False,
        permission_classes=(SIAPermissions,),
        source='type_assignment',
    )

    directing_departments = _NestedDepartmentModelSerializer(
        source='directing_departments_assignment.departments',
        many=True,
        required=False,
        permission_classes=(SIAPermissions,),
    )

    updates = SignalPlanUpdateSerializer(
        many=True, 
        required=False
    )

    has_attachments = serializers.SerializerMethodField()

    extra_properties = SignalExtraPropertiesField(
        required=False,
        validators=[
            ExtraPropertiesValidator(filename=os.path.join(
                os.path.dirname(__file__), '..', 'json_schema', 'extra_properties.json')
            )
        ]
    )  # noqa

    class Meta:
        model = Signal
        fields = (
            '_links',
            '_display',
            'category',
            'id',
            'has_attachments',
            'location',
            'status',
            'reporter',
            'priority',
            'notes',
            'type',
            'source',
            'text',
            'text_extra',
            'extra_properties',
            'created_at',
            'updated_at',
            'incident_date_start',
            'incident_date_end',
            'finished_by',
            'directing_departments',
            'country',
            'city',
            'city_object',
            'webform_kenmark',
            'mb_report_id',
            'facilitator_report_id',
            'report_days',
            'forman_emp_name',
            'urgency',
            'plan_time',
            'updates',
        )
        read_only_fields = (
            'id',
            'has_attachments',
        )

    def get_has_attachments(self, obj):
        return obj.attachments.exists()

    def update(self, instance, validated_data):
        """
        Perform update on nested models.

        Note:
        - Reporter cannot be updated via the API.
        - Atomic update (all fail/succeed), django signals on full success (see
          underlying update_multiple method of actions SignalManager).
        """
        if not instance.is_parent() and validated_data.get('directing_departments_assignment') is not None:
            raise serializers.ValidationError('Directing departments can only be set on a parent Signal')

        user_email = self.context['request'].user.email

        for _property in ['location', 'status', 'category_assignment', 'priority']:
            if _property in validated_data:
                data = validated_data[_property]
                data['created_by'] = user_email

        if 'type_assignment' in validated_data:
            type_data = validated_data.pop('type_assignment')
            type_data['created_by'] = user_email
            validated_data['type'] = type_data

        if 'notes' in validated_data and validated_data['notes']:
            note_data = validated_data['notes'][0]
            note_data['created_by'] = user_email

        if 'directing_departments_assignment' in validated_data and validated_data['directing_departments_assignment']:
            validated_data['directing_departments_assignment']['created_by'] = user_email

        signal = Signal.actions.update_multiple(validated_data, instance)
        return signal


class PrivateSignalSerializerList(HALSerializer, AddressValidationMixin):
    """
    This serializer is used for the list endpoint and when creating a new instance
    """
    serializer_url_field = PrivateSignalLinksField
    _display = DisplayField()

    country = CountrySerializer(
        required=False,
        permission_classes=(SIAPermissions,)
    )

    city = CitySerializer(
        required=False,
        permission_classes=(SIAPermissions,)
    )

    city_object = CityObjectSerializer(
        many=True,
        required=False
    )

    location = _NestedLocationModelSerializer(
        permission_classes=(SIAPermissions,)
    )

    status = _NestedStatusModelSerializer(
        required=False,
        permission_classes=(SignalCreateInitialPermission,)
    )

    category = _NestedCategoryModelSerializer(
        source='category_assignment',
        permission_classes=(SignalCreateInitialPermission,)
    )

    reporter = _NestedReporterModelSerializer(
        permission_classes=(SIAPermissions,)
    )

    priority = _NestedPriorityModelSerializer(
        required=False,
        permission_classes=(SIAPermissions,)
    )

    notes = _NestedNoteModelSerializer(
        many=True,
        required=False,
        permission_classes=(SignalCreateInitialPermission,)
    )

    type = _NestedTypeModelSerializer(
        required=False,
        permission_classes=(SIAPermissions,),
        source='type_assignment',
    )

    updates = SignalPlanUpdateSerializer(
        many=True, 
        required=False
    )

    directing_departments = _NestedDepartmentModelSerializer(
        source='directing_departments_assignment.departments',
        many=True,
        required=False,
        permission_classes=(SIAPermissions,),
    )

    has_attachments = serializers.SerializerMethodField()

    extra_properties = SignalExtraPropertiesField(
        required=False,
        allow_null=True,
        validators=[
            ExtraPropertiesValidator(
                filename=os.path.join(
                    os.path.dirname(__file__), '..', 'json_schema', 'extra_properties.json')
            )
        ]
    )

    class Meta:
        model = Signal
        fields = (
            '_links',
            '_display',
            'id',
            'signal_id',
            'source',
            'text',
            'text_extra',
            'status',
            'location',
            'category',
            'reporter',
            'priority',
            'type',
            'created_at',
            'updated_at',
            'incident_date_start',
            'incident_date_end',
            'operational_date',
            'has_attachments',
            'extra_properties',
            'notes',
            'directing_departments',
            'finished_by',
            'country',
            'city',
            'city_object',
            'webform_kenmark',
            'mb_report_id',
            'facilitator_report_id',
            'report_days',
            'forman_emp_name',
            'urgency',
            'plan_time',
            'updates',
        )
        read_only_fields = (
            'created_at',
            'updated_at',
            'has_attachments',
        )
        extra_kwargs = {
            'source': {'validators': [SignalSourceValidator()]},
        }

    def get_has_attachments(self, obj):
        return obj.attachments.exists()

    def create(self, validated_data):
        if validated_data.get('directing_departments_assignment') is not None:
            raise serializers.ValidationError('Directing departments cannot be set on initial creation')

        if validated_data.get('status') is not None:
            raise serializers.ValidationError("Status cannot be set on initial creation")

        # Set default status
        logged_in_user = self.context['request'].user
        INITIAL_STATUS = {
            'state': workflow.GEMELD,  # see models.py is already default
            'text': None,
            'user': logged_in_user.email,
        }

        # We require location and reporter to be set and to be valid.
        reporter_data = validated_data.pop('reporter')

        location_data = validated_data.pop('location')
        location_data['created_by'] = logged_in_user.email

        category_assignment_data = validated_data.pop('category_assignment')
        category_assignment_data['created_by'] = logged_in_user.email

        # We will use the priority and signal type on the incoming message if present.
        priority_data = validated_data.pop('priority', {
            'priority': Priority.PRIORITY_NORMAL
        })
        priority_data['created_by'] = logged_in_user.email
        type_data = validated_data.pop('type_assignment', {})
        type_data['created_by'] = logged_in_user.email

        country_data = validated_data.pop('country', None)
        city_data = validated_data.pop('city', None)
        city_object_data = validated_data.pop('city_object', None)

        signal = Signal.actions.create_initial(
            validated_data,
            location_data,
            INITIAL_STATUS,
            category_assignment_data,
            reporter_data,
            country_data,
            city_data,
            city_object_data,
            priority_data,
            type_data
        )

        return signal


class PublicSignalSerializerDetail(HALSerializer):
    #status = _NestedPublicStatusModelSerializer(required=False)
    status = _NestedStatusModelSerializer(required=False)
    serializer_url_field = PublicSignalLinksField
    _display = serializers.SerializerMethodField(method_name='get__display')
    country = serializers.SerializerMethodField(required=False)
    city = serializers.SerializerMethodField(required=False)
    city_object = CityObjectSerializer(
        many=True,
        required=False
    )
    category = _NestedCategoryModelSerializer(
        source='category_assignment',
        required=False,
    )

    directing_departments = _NestedDepartmentModelSerializer(
        source='directing_departments_assignment.departments',
        many=True,
        required=False,
    )

    updates = SignalPlanUpdateSerializer(
        many=True, 
        required=False
    )

    location = _NestedLocationModelSerializer(
        required=False,
    )

    incident_date_start = serializers.DateTimeField(required=False)
    #id_mapping = IDMappingSerializer(required=False)
    text = serializers.CharField(required=False)

    class Meta:
        model = Signal
        fields = (
            '_display',
            'id',
            'text',
            'signal_id',
            'status',
            'created_at',
            'updated_at',
            'incident_date_start',
            'incident_date_end',
            'finished_by',
            'country',
            'city',
            'city_object',
            'category',
            'directing_departments',
            'schedule_datetime',
            'webform_kenmark',
            'mb_report_id',
            'facilitator_report_id',
            'report_days',
            'forman_emp_name',
            'urgency',
            'plan_time',
            'updates',
            'location',
        )

    def get__display(self, obj):
        return obj.sia_id


    def get_country(self, obj):
        if obj.country and obj.country.country_name:
            return CountrySerializer(
                Country.objects.get(country_name__iexact=obj.country.country_name)
            ).data

        return None

    def get_city(self, obj):
        if obj.city and obj.city.city_name:
            return CitySerializer(
                City.objects.get(city_name__iexact=obj.city.city_name)
            ).data

        return None

    def update(self, instance, validated_data):
        # user_email = self.context['request'].user.email
        # print(validated_data)

        user_email = "signals.admin@example.com"

        for _property in ['location', 'status', 'category_assignment', 'priority']:
            if _property in validated_data:
                data = validated_data[_property]
                data['created_by'] = user_email

        if 'type_assignment' in validated_data:
            type_data = validated_data.pop('type_assignment')
            type_data['created_by'] = user_email
            validated_data['type'] = type_data

        if 'notes' in validated_data and validated_data['notes']:
            note_data = validated_data['notes'][0]
            note_data['created_by'] = user_email

        if 'directing_departments_assignment' in validated_data and validated_data['directing_departments_assignment']:
            validated_data['directing_departments_assignment']['created_by'] = user_email

        signal = Signal.actions.update_multiple(validated_data, instance)
        return signal




class PublicSignalCreateSerializer(serializers.ModelSerializer):
    """
    This serializer allows anonymous users to report `signals.Signals`.

    Note: this is only used in the creation of new Signal instances, not to
    create the response body after a succesfull POST.
    """
    status = _NestedStatusModelSerializer(
        required=False,
    )
    location = _NestedLocationModelSerializer()
    reporter = _NestedReporterModelSerializer()
    category = _NestedCategoryModelSerializer(source='category_assignment')

    country = CountrySerializer(required=False)
    city = CitySerializer(required=False)
    city_object = CityObjectSerializer(
        many=True,
        required=False
    )

    updates = SignalPlanUpdateSerializer(
        many=True, 
        required=False
    )

    extra_properties = SignalExtraPropertiesField(
        required=False,
        allow_null=True,
        validators=[
            ExtraPropertiesValidator(
                filename=os.path.join(
                    os.path.dirname(__file__), '..', 'json_schema', 'extra_properties.json'
                )
            )
        ]
    )

    incident_date_start = serializers.DateTimeField()
    #id_mapping = IDMappingSerializer(required=False)

    class Meta(object):
        model = Signal
        fields = (
            'text',
            'text_extra',
            'signal_id',
            'location',
            'category',
            'reporter',
            'incident_date_start',
            'incident_date_end',
            'status',
            'source',
            'extra_properties',
            'country',
            'city',
            'city_object',
            'webform_kenmark',
            'mb_report_id',
            'facilitator_report_id',
            'report_days',
            'forman_emp_name',
            'urgency',
            'plan_time',
            'updates',
        )

    def validate(self, data):
        """Make sure any extra data is rejected"""
        if hasattr(self, 'initial_data'):
            present_keys = set(self.initial_data)
            allowed_keys = set(self.fields)

            if present_keys - allowed_keys:
                raise ValidationError('Extra properties present: {}'.format(
                    ', '.join(present_keys - allowed_keys)
                ))
        return data

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        reporter_data = validated_data.pop('reporter')
        category_assignment_data = validated_data.pop('category_assignment')
        country_data = validated_data.pop('country', None)
        city_data = validated_data.pop('city', None)
        city_object_data = validated_data.pop('city_object', None)
        status_data = validated_data.pop('status', None)
        if not status_data:
            status_data = {"state": workflow.GEMELD}

        signal = Signal.actions._create_initial_no_transaction(
            validated_data, location_data, status_data, category_assignment_data, reporter_data, country_data, city_data, city_object_data)
        return signal


class SignalIdListSerializer(HALSerializer):
    class Meta:
        model = Signal
        fields = (
            'id',
        )


class SignalGeoSerializer(GeoFeatureModelSerializer):
    # For use with the "geography" action
    location = GeometryField(source='location.geometrie')

    class Meta:
        model = Signal
        id_field = False
        geo_field = 'location'
        fields = ['id', 'created_at']


class AbridgedChildSignalSerializer(HALSerializer):
    serializer_url_field = PrivateSignalLinksField

    status = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Signal
        fields = (
            '_links',
            'id',
            'status',
            'category',
        )

    def get_status(self, obj):
        return {
            'state': obj.status.state,
            'state_display': obj.status.get_state_display(),
        }

    def get_category(self, obj):
        departments = ', '.join(
            obj.category_assignment.category.departments.filter(
                categorydepartment__is_responsible=True
            ).values_list('code', flat=True)
        )
        return {
            'sub': obj.category_assignment.category.name,
            'sub_slug': obj.category_assignment.category.slug,
            'departments': departments,
            'main': obj.category_assignment.category.parent.name,
            'main_slug': obj.category_assignment.category.parent.slug,
        }
