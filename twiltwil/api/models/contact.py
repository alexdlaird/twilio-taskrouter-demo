"""
Contact model.
"""

__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import logging

import phonenumbers
from django.db import models

from twiltwil.common.models.base import BaseModel

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
            name = f'{name} {self.last_name}'.strip()

        details = []
        if self.phone_number:
            formatted_number = phonenumbers.format_number(phonenumbers.parse(self.phone_number),
                                                      phonenumbers.PhoneNumberFormat.NATIONAL)
            details.append(f'P: {formatted_number}')
        if self.email:
            details.append(f'E: {self.email}')
        details = ', '.join(details)

        if name and details:
            return f'{name} ({details})'
        else:
            return details
