from signals.apps.api.generics import mixins
from signals.apps.signals.models import Neighbourhood, District, PostCode
from signals.apps.api.v1.serializers.nested.district import _NestedDistrictSerializer
from signals.apps.api.v1.serializers.neighbourhood import NeighbourhoodSerializer
from signals.apps.api.v1.serializers.postcode import PostCodeSerializer

from datapunt_api.rest import DatapuntViewSet, HALPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets


class PrivatePostCodeViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = PostCodeSerializer
    queryset = PostCode.objects.all()

    def list(self, *args, **kwargs):
        neighs = PostCode.objects.all()
        serializer = PostCodeSerializer(
            neighs, many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


    def retrieve(self, request, postcode_id):
        try:
            postcode = PostCode.objects.get(id=postcode_id)
            data = PostCodeSerializer(postcode).data
            return Response(data, status=status.HTTP_200_OK)
            
        except PostCode.DoesNotExist:
            data = {
                "error": "Please enter valid ID"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
    

    def create(self, request):
        # print("View: ", request.data)
        serializer = PostCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        postCode = serializer.save()

        data = PostCodeSerializer(postCode).data
        return Response(data, status=status.HTTP_201_CREATED)

