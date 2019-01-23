import logging

from django.contrib.auth import get_user_model
from rest_framework import serializers

__author__ = "Alex Laird"
__copyright__ = 'Copyright 2018, Alex Lair'
__version__ = "0.1.0"

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'worker_sid', 'time_zone', 'languages', 'skills',)
