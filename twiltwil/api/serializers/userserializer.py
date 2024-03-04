__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import logging

from django.contrib.auth import get_user_model
from rest_framework import serializers

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'worker_sid', 'time_zone', 'languages', 'skills',)
