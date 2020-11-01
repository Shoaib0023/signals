from signals.apps.api.generics import mixins
from signals.apps.signals.models.id_mapping import IDMapping
from signals.apps.api.v1.serializers.id_mapping import IDMappingSerializer
from datapunt_api.rest import DatapuntViewSet, HALPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets


class IDMappingViewset(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, GenericViewSet):
    serializer_class = IDMappingSerializer
    lookup_field = 'seda_signal_id'

    def list(self, *args, **kwargs):
        mapping = IDMapping.objects.all()
        serializer = IDMappingSerializer(mapping, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
    def retrieve(self, request, seda_signal_id):
        print(seda_signal_id)
        mapping = IDMapping.objects.get(mb_signal_id=seda_signal_id)
        data = IDMappingSerializer(mapping, context=self.get_serializer_context()).data
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = IDMappingSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        mapping = serializer.save()

        data = IDMappingSerializer(mapping, context=self.get_serializer_context()).data
        return Response(data , status=status.HTTP_201_CREATED)


    def update(self, request, seda_signal_id):
        #print(seda_signal_id)
        instance = IDMapping.objects.get(seda_signal_id=seda_signal_id)
        serializer = IDMappingSerializer(instance, data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
