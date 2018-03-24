"""
Skill model.
"""

import logging

from django.db import models
from django.db.models import Model

from twiltwil.common import enums
from twiltwil.common.models.base import BaseModel

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)


class Skill(Model):
    id = models.CharField(max_length=30, primary_key=True)

    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
