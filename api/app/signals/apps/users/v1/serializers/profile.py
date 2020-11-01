from rest_framework import serializers

from signals.apps.signals.models import Department
from signals.apps.users.models import Profile

from signals.apps.signals.models.country import Country
from signals.apps.signals.models.city import City
from signals.apps.api.v1.serializers.city import CitySerializer
from signals.apps.api.v1.serializers.country import CountrySerializer


def _get_departments_queryset():
    return Department.objects.all()


class ProfileListSerializer(serializers.ModelSerializer):
    departments = serializers.SerializerMethodField()
    department_ids = serializers.PrimaryKeyRelatedField(
        many=True, required=False, read_only=False, write_only=True,
        queryset=_get_departments_queryset(), source='departments'
    )

    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'note',
            'departments',
            'department_ids',
            'created_at',
            'updated_at',
            'country',
            'city',
            '_type'
        )

    def get_departments(self, obj):
        return obj.departments.values_list('name', flat=True)

    def get_country(self, obj):
        if obj.country:
            return CountrySerializer(
                Country.objects.get(id=obj.country.id)
            ).data

        return None

    def get_city(self, obj):
        if obj.city:
            return CitySerializer(
                City.objects.get(id=obj.city.id)
            ).data

        return None


class ProfileDetailSerializer(serializers.ModelSerializer):
    departments = serializers.SerializerMethodField()
    department_ids = serializers.PrimaryKeyRelatedField(
        many=True, required=False, read_only=False, write_only=True,
        queryset=_get_departments_queryset(), source='departments'
    )

    city = CitySerializer()
    country = CountrySerializer()

    class Meta:
        model = Profile
        fields = (
            'note',
            'departments',
            'department_ids',
            'created_at',
            'updated_at',
            'city',
            'country',
            '_type'
        )

    def get_departments(self, obj):
        return obj.departments.values_list('name', flat=True)

    def update(self, instance, validated_data):
        city_data = validated_data.pop('city')
        country_data = validated_data.pop('country')

        if Country.objects.filter(country_name__iexact=country_data["country_name"]).exists():
            country = Country.objects.get(country_name__iexact=country_data["country_name"])
            instance.country = country

        else:
            country = Country.objects.create(**country_data)
            instance.country = country

        if City.objects.filter(city_name__iexact=city_data["city_name"]).exists():
            city = City.objects.get(city_name__iexact=city_data["city_name"])
            instance.city = city

        else:
            city = City.objects.create(**city_data)
            instance.city = city

        instance = super(ProfileDetailSerializer, self).update(instance, validated_data)

        instance.refresh_from_db()
        return instance
