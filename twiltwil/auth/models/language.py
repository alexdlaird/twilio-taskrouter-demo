"""
Language model.
"""

import logging

from django.db import models
from django.db.models import Model

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.1.0"

logger = logging.getLogger(__name__)


class Language(Model):
    id = models.CharField(max_length=20, primary_key=True)

    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
