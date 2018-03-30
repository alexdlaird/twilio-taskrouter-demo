"""
Message model.
"""

import logging

from django.db import models

from twiltwil.api.managers.messagemanager import MessageManager
from twiltwil.common import enums
from twiltwil.common.models.base import BaseModel

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)


class Message(BaseModel):
    sid = models.CharField(max_length=255)

    channel = models.CharField(max_length=15, choices=enums.CHANNEL_CHOICES)

    sender = models.CharField(max_length=255)

    receiver = models.CharField(max_length=255)

    direction = models.CharField(max_length=8, choices=enums.MESSAGE_DIRECTION_CHOICES)

    status = models.CharField(max_length=15, choices=enums.MESSAGE_STATUS_CHOICES)

    text = models.TextField(blank=True)

    addons = models.TextField(blank=True, null=True)

    raw = models.TextField(blank=True, null=True)

    task_sid = models.CharField(max_length=255, blank=True, null=True)

    worker_sid = models.CharField(max_length=255, blank=True, null=True)

    resolved = models.BooleanField(default=False)

    # Set the manager
    objects = MessageManager()
