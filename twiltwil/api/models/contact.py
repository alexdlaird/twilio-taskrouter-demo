"""
Contact model.
"""

import logging

import phonenumbers
from django.db import models

from twiltwil.common.models.base import BaseModel

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"

logger = logging.getLogger(__name__)


class Contact(BaseModel):
    uuid = models.UUIDField(unique=True)

    first_name = models.CharField(max_length=50, blank=True, null=True)

    last_name = models.CharField(max_length=50, blank=True, null=True)

    phone_number = models.CharField(max_length=15, unique=True)

    email = models.EmailField(blank=True, null=True, unique=True)

    @property
    def card(self):
        name = ''
        if self.first_name:
            name += self.first_name
        if self.last_name:
            name = '{} {}'.format(name, self.last_name).strip()

        details = []
        if self.phone_number:
            details.append('P: {}'.format(phonenumbers.format_number(phonenumbers.parse(self.phone_number),
                                                                     phonenumbers.PhoneNumberFormat.NATIONAL)))
        if self.email:
            details.append('E: {}'.format(self.email))
        details = ', '.join(details)

        if name and details:
            return '{} ({})'.format(name, details)
        else:
            return details
