from datapunt_api.rest import DisplayField, HALSerializer
from rest_framework import serializers

from signals.apps.signals.models import ImageCategory


class ImageCategorySerializer(HALSerializer):
    class Meta:
        model = ImageCategory
        fields = (
            'category_level_name1',
            'category_level_name2',
            'category_level_name3',
            'category_level_name4',
        )
