import logging

from rest_framework import serializers

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.1"

logger = logging.getLogger(__name__)


class InfoSerializer(serializers.Serializer):
    name = serializers.CharField()

    version = serializers.CharField()

    disable_lobby_video = serializers.BooleanField()

    conference_status_callback_url = serializers.URLField()

    max_http_retries = serializers.IntegerField()

    api_base_url = serializers.URLField()

    event_bridge_base_url = serializers.URLField()

    region = serializers.CharField()
