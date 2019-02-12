import logging

from rest_framework import serializers

from twiltwil.api.models import Contact

__author__ = "Alex Laird"
__copyright__ = 'Copyright 2018, Alex Lair'
__version__ = "0.1.0"

logger = logging.getLogger(__name__)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'uuid', 'first_name', 'last_name', 'phone_number', 'email', 'card',)
