from rest_framework import serializers

from signals.apps.api.generics.serializers import SIAModelSerializer
from signals.apps.api.v1.fields import (
    CategoryHyperlinkedRelatedField,
    LegacyCategoryHyperlinkedRelatedField
)
from signals.apps.signals.models import CategoryAssignment


class _NestedCategoryModelSerializer(SIAModelSerializer):
    sub = serializers.CharField(source='category.name', read_only=True)
    sub_slug = serializers.CharField(source='category.slug', read_only=True)
    main = serializers.CharField(source='category.parent.name', read_only=True)
    main_slug = serializers.CharField(source='category.parent.slug', read_only=True)

    # sub_category = LegacyCategoryHyperlinkedRelatedField(source='category',
    #                                                      write_only=True,
    #                                                      required=False)
    category_url = CategoryHyperlinkedRelatedField(source='category',
                                                   required=False)

    text = serializers.CharField(required=False)
    departments = serializers.SerializerMethodField()
    category_level_name1 = serializers.CharField(source='category.category_level_name1', read_only=True)
    category_level_name2 = serializers.CharField(source='category.category_level_name2', read_only=True)
    category_level_name3 = serializers.CharField(source='category.category_level_name3', read_only=True)
    category_level_name4 = serializers.CharField(source='category.category_level_name4', read_only=True)


    class Meta:
        model = CategoryAssignment
        fields = (
            # 'sub_category',
            'sub',
            'sub_slug',
            'main',
            'main_slug',
            'category_url',
            'departments',
            'created_by',
            'text',
            'category_level_name1',
            'category_level_name2',
            'category_level_name3',
            'category_level_name4',
        )
        read_only_fields = (
            'sub',
            'sub_slug',
            'main',
            'main_slug',
            'created_by',
            'departments',
            'category_level_name1',
            'category_level_name2',
            'category_level_name3',
            'category_level_name4',
        )

    def get_departments(self, obj):
        return ', '.join(
            obj.category.departments.filter(categorydepartment__is_responsible=True).values_list('code', flat=True)
        )
