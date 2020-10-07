from datapunt_api.rest import DisplayField, HALSerializer
from rest_framework import routers, serializers, viewsets, status
from datapunt_api.rest import DatapuntViewSet, HALPagination

from signals.apps.api.generics import mixins
from rest_framework import status
from rest_framework.response import Response

from signals.apps.signals.models import SignalPlanUpdate
from signals.apps.api.v1.serializers import SignalPlanUpdateSerializer


class SignalPlanUpdateViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, DatapuntViewSet):
    queryset = SignalPlanUpdate.objects.all()
    serializer_class = SignalPlanUpdateSerializer
    serializer_detail_class = SignalPlanUpdateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_detail_class(data=request.data,
                                                    context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

