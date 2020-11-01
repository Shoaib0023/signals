from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from signals.apps.api.generics import mixins
from rest_framework.response import Response

from signals.apps.signals.models import District, PostCode
from signals.apps.api.v1.serializers.nested.postcode import _NestedPostCodeSerializer

import json

class PrivateStadsdeelViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = _NestedPostCodeSerializer

    def list(self, request, post_code):
        if PostCode.objects.filter(post_code=post_code).exists():
            postcode = PostCode.objects.get(post_code=post_code)
            serializer = _NestedPostCodeSerializer(postcode)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if ''.join(post_code.split()) == post_code and len(post_code) > 2:
            post_code = post_code[0:len(post_code)-2] + ' ' + post_code[-2:]
            #print("222")
            if PostCode.objects.filter(post_code=post_code).exists():
                postcode = PostCode.objects.get(post_code=post_code)
                serializer = _NestedPostCodeSerializer(postcode)
                return Response(serializer.data, status=status.HTTP_200_OK)


        error = {
            "error": "Invalid Postcode",
            "stadsdeel": {
                   "name": ""
            }
        }

        return Response(error, status=status.HTTP_404_NOT_FOUND)
