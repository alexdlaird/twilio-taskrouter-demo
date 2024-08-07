__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import logging

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from twiltwil.api.models import Contact
from twiltwil.api.serializers.contactserializer import ContactSerializer

logger = logging.getLogger(__name__)


class ContactView(GenericAPIView, RetrieveModelMixin):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "uuid"

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = self.get_serializer(user)

        return Response(serializer.data)
