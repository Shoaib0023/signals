from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from signals.apps.api.generics import mixins
from signals.apps.api.generics.permissions import ModelWritePermissions, SIAPermissions
from signals.apps.api.v1.serializers import StateStatusMessageTemplateSerializer
from signals.apps.signals.models import Category, StatusMessageTemplate
from signals.auth.backend import JWTAuthBackend


class StatusMessageTemplatesViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                                    viewsets.GenericViewSet):
    serializer_class = StateStatusMessageTemplateSerializer

    authentication_classes = (JWTAuthBackend,)
    permission_classes = (SIAPermissions & ModelWritePermissions,)
    pagination_class = None

    queryset = StatusMessageTemplate.objects.none()

    def get_object(self):
        if 'cat4' in self.kwargs:
            kwargs = {'category_level_name1': self.kwargs["cat1"], 'category_level_name2': self.kwargs["cat2"], 'category_level_name3': self.kwargs["cat3"], 'category_level_name4': self.kwargs["cat4"]}

        elif 'cat3' in self.kwargs:
            kwargs = {'category_level_name1': self.kwargs["cat1"], 'category_level_name2': self.kwargs["cat2"], 'category_level_name3': self.kwargs["cat3"]}

        elif 'cat2' in self.kwargs:
            kwargs = {'category_level_name1': self.kwargs["cat1"], 'category_level_name2': self.kwargs["cat2"]}

        else:
            kwargs = {'category_level_name1': self.kwargs["cat1"]}

        if self.request.method == "POST":
            obj = Category.objects.get(**kwargs)
        else:
            obj = Category.objects.filter(**kwargs)

        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_context(self):
        context = super(StatusMessageTemplatesViewSet, self).get_serializer_context()
        context.update({'category': self.get_object()})
        return context

    def retrieve(self, request, *args, **kwargs):
        if request.method == "POST":
            status_message_templates = self.get_object().status_message_templates.all()
            serializer = self.get_serializer(status_message_templates, many=True)
            return Response(serializer.data)

        else:
            status_message_templates = [category.status_message_templates.all() for category in self.get_object()]
            result = []
            for category in self.get_object():
                status_message_templates = category.status_message_templates.all()
                serializer = self.get_serializer(status_message_templates, many=True)
                result.extend(serializer.data)

            return Response(result)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return self.retrieve(request, *args, **kwargs)
