from signals.apps.api.generics import mixins
from signals.apps.signals.models.district import District
from signals.apps.api.v1.serializers.nested.district import _NestedDistrictSerializer
from datapunt_api.rest import DatapuntViewSet, HALPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets

from signals.auth.backend import JWTAuthBackend
from signals.apps.api.generics.permissions import ModelWritePermissions, SIAPermissions


class PrivateDistrictViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = _NestedDistrictSerializer
    queryset = District.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    authentication_classes = (JWTAuthBackend,)
    permission_classes = (SIAPermissions & ModelWritePermissions, )

    def list(self, *args, **kwargs):
        districts = District.objects.all()
        serializer =  _NestedDistrictSerializer(
                districts, many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


    def retrieve(self, request, id):
        try:
            district = District.objects.get(id=id)
            data = _NestedDistrictSerializer(district).data
            return Response(data, status=status.HTTP_200_OK)
            
        except District.DoesNotExist:
            data = {
                "error": "Please enter valid ID"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    
    def create(self, request):
        serializer = _NestedDistrictSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        district = serializer.save()

        data = _NestedDistrictSerializer(district).data
        return Response(data, status=status.HTTP_201_CREATED)

