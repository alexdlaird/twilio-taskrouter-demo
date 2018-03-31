"""
Contact model.
"""

import logging

from django.db import models

from twiltwil.common.models.base import BaseModel

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)


class Contact(BaseModel):
    sid = models.CharField(max_length=255, unique=True)

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    phone_number = models.CharField(max_length=15, unique=True)

    email = models.EmailField(unique=True)
