import logging

from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from twiltwil.api.serializers.userserializer import UserSerializer

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.1.0"

logger = logging.getLogger(__name__)


class UserView(GenericAPIView, RetrieveModelMixin):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = self.get_serializer(user)

        return Response(serializer.data)
