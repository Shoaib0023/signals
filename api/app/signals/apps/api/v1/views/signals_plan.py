from datapunt_api.rest import DatapuntViewSet, HALPagination
from rest_framework import status
from rest_framework.response import Response

from signals.apps.api.generics import mixins
from signals.apps.api.generics.permissions import ModelWritePermissions, SIAPermissions
from signals.apps.api.v1.serializers.signals_plan import PrivateSignalsPlanSerializerList, PrivateSignalsPlanSerializerDetail
from signals.apps.signals.models.signals_plan import SignalsPlan
from signals.auth.backend import JWTAuthBackend


class PrivateSignalsPlanViewset(mixins.ListModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.CreateModelMixin,
                               mixins.UpdateModelMixin,
                               DatapuntViewSet):
    queryset = SignalsPlan.objects.all()

    serializer_class = PrivateSignalsPlanSerializerList
    serializer_detail_class = PrivateSignalsPlanSerializerDetail

    pagination_class = HALPagination

    authentication_classes = (JWTAuthBackend,)
    permission_classes = (SIAPermissions & ModelWritePermissions, )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_detail_class(data=request.data,
                                                  context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
