from signals.apps.api.generics import mixins
from signals.apps.signals.models import Neighbourhood, District
from signals.apps.api.v1.serializers.nested.district import _NestedDistrictSerializer
from signals.apps.api.v1.serializers.neighbourhood import NeighbourhoodSerializer

from datapunt_api.rest import DatapuntViewSet, HALPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets

from signals.auth.backend import JWTAuthBackend
from signals.apps.api.generics.permissions import ModelWritePermissions, SIAPermissions


class PrivateNeighbourhoodViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = NeighbourhoodSerializer
    queryset = Neighbourhood.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    authentication_classes = (JWTAuthBackend,)
    permission_classes = (SIAPermissions & ModelWritePermissions, )

    def list(self, *args, **kwargs):
        neighs = Neighbourhood.objects.all()
        serializer =  NeighbourhoodSerializer(
                neighs, many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def retrieve(self, request, id):
        try:
            neigh = Neighbourhood.objects.get(id=id)
            data = NeighbourhoodSerializer(neigh).data
            return Response(data, status=status.HTTP_200_OK)
            
        except Neighbourhood.DoesNotExist:
            data = {
                "error": "Please enter valid ID"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        

    def create(self, request):
        # print("View: ", request.data)
        serializer = NeighbourhoodSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        neighbourhood = serializer.save()

        data = NeighbourhoodSerializer(neighbourhood).data
        return Response(data, status=status.HTTP_201_CREATED)

