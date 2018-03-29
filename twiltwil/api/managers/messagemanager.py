"""
Manager for the Message model.
"""

import logging

from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models import Q

from twiltwil.common import enums

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)


class MessageQuerySet(models.query.QuerySet):
    def for_number(self, number):
        return self.filter(
            Q(direction=enums.MESSAGE_OUTBOUND, receiver=number) | Q(direction=enums.MESSAGE_INBOUND, sender=number))

    def for_channel(self, channel):
        return self.filter(channel=channel)

    def for_task(self, task_sid):
        return self.filter(task_sid=task_sid)

    def for_worker(self, worker_sid):
        return self.filter(worker_sid=worker_sid)


class MessageManager(BaseUserManager):
    def get_queryset(self):
        return MessageQuerySet(self.model, using=self._db)

    def for_number(self, number):
        self.get_queryset().for_number(number)

    def for_channel(self, channel):
        self.get_queryset().for_channel(channel)

    def for_task(self, task_sid):
        self.get_queryset().for_task(task_sid)

    def for_worker(self, worker_sid):
        self.get_queryset().for_worker(worker_sid)
