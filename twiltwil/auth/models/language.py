"""
Language model.
"""

__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import logging

from django.db import models
from django.db.models import Model

logger = logging.getLogger(__name__)


class Language(Model):
    id = models.CharField(max_length=20, primary_key=True)

    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
