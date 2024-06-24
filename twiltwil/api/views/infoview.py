__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import logging

from django.conf import settings
from django.urls import reverse
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response

from twiltwil.api.serializers.infoserializer import InfoSerializer

logger = logging.getLogger(__name__)


class InfoView(GenericAPIView, RetrieveModelMixin):
    def get(self, request, *args, **kwargs):
        serializer = InfoSerializer({
            "name": settings.PROJECT_NAME,
            "version": settings.PROJECT_VERSION,
            "disable_lobby_video": settings.DISABLE_LOBBY_VIDEO,
            "conference_status_callback_url": settings.PROJECT_HOST + reverse("api_webhooks_voice_conference"),
            "max_http_retries": settings.MAX_HTTP_RETRIES,
            "api_base_url": settings.TWILIO_API_BASE_URL,
            "event_bridge_base_url": settings.TWILIO_EVENT_BRIDGE_BASE_URL,
            "region": settings.TWILIO_REGION,
        })

        return Response(serializer.data)
