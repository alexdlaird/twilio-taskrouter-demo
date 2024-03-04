__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import logging

from rest_framework import serializers

from twiltwil.api.models import Contact

logger = logging.getLogger(__name__)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'uuid', 'first_name', 'last_name', 'phone_number', 'email', 'card',)
