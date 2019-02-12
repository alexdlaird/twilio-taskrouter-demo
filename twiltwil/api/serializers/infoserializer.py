import logging

from rest_framework import serializers

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"

logger = logging.getLogger(__name__)


class InfoSerializer(serializers.Serializer):
    name = serializers.CharField()

    version = serializers.CharField()

    conference_status_callback_url = serializers.URLField()
