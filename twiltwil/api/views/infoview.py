import logging

from django.conf import settings
from django.urls import reverse
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response

from twiltwil.api.serializers.infoserializer import InfoSerializer

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"

logger = logging.getLogger(__name__)


class InfoView(GenericAPIView, RetrieveModelMixin):
    def get(self, request, *args, **kwargs):
        serializer = InfoSerializer({
            'name': settings.PROJECT_NAME,
            'version': settings.PROJECT_VERSION,
            'conference_status_callback_url': settings.PROJECT_HOST + reverse('api_webhooks_voice_conference'),
        })

        return Response(serializer.data)
