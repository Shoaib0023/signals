from signals.apps.api.generics import mixins
from signals.apps.signals.models import ImageCategory, Signal
from signals.apps.api.v1.serializers.image_category import ImageCategorySerializer
from django.http import Http404

from datapunt_api.rest import DatapuntViewSet, HALPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets


class PublicImageCategoryViewset(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    serializer_class = ImageCategorySerializer
    queryset = ImageCategory.objects.all()

    def list(self, *args, **kwargs):
        raise Http404()

    def create(self, request):
        signal_id = request.data["signal_id"]
        signal = Signal.objects.get(signal_id=signal_id)

        serializer = ImageCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        signal.image_category = category
        signal.save()

        data = ImageCategorySerializer(category).data
        return Response(data, status=status.HTTP_201_CREATED)

