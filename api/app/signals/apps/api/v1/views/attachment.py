"""
Views dealing with 'signals.Attachment' model directly.
"""
from datapunt_api.pagination import HALPagination
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin

from signals.apps.api.generics import mixins
from signals.apps.api.generics.permissions import SIAPermissions
from signals.apps.api.v1.serializers import (
    PrivateSignalAttachmentSerializer,
    PublicSignalAttachmentSerializer
)
from signals.apps.api.v1.views._base import PublicSignalGenericViewSet
from signals.apps.signals.models import Attachment, Signal
from signals.auth.backend import JWTAuthBackend
from rest_framework.response import Response
from rest_framework import status
from signals.apps.api.v1.serializers.nested import _NestedAttachmentModelSerializer


class PublicSignalAttachmentsViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, PublicSignalGenericViewSet):
    serializer_class = PublicSignalAttachmentSerializer

    def list(self, request, signal_id):
        signal = Signal.objects.get(signal_id=signal_id)
        attachments = Attachment.objects.filter(_signal=signal)
        serializer = _NestedAttachmentModelSerializer(attachments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PrivateSignalAttachmentsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                                      viewsets.GenericViewSet):
    serializer_class = PrivateSignalAttachmentSerializer
    pagination_class = HALPagination
    queryset = Attachment.objects.all()

    lookup_url_kwarg = 'pk'

    authentication_classes = (JWTAuthBackend,)
    permission_classes = (SIAPermissions,)

    def _filter_kwargs(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        return {self.lookup_field: self.kwargs[lookup_url_kwarg]}

    def get_object(self):
        self.lookup_field = self.lookup_url_kwarg

        obj = get_object_or_404(Signal.objects.all(), **self._filter_kwargs())
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        self.lookup_field = '_signal_id'

        qs = super(PrivateSignalAttachmentsViewSet, self).get_queryset()
        return qs.filter(**self._filter_kwargs())
