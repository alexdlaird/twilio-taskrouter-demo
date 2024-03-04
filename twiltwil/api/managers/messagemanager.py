"""
Manager for the Message model.
"""

__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import logging

from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models import Q

from twiltwil.common import enums

logger = logging.getLogger(__name__)


class MessageQuerySet(models.query.QuerySet):
    def inbound(self):
        return self.filter(direction=enums.MESSAGE_INBOUND)

    def not_resolved(self):
        return self.exclude(resolved=True)

    def has_task(self):
        return self.exclude(task_sid__isnull=True)

    def no_worker(self):
        return self.filter(worker_sid__isnull=True)

    def for_contact(self, uuid):
        return self.filter(
            Q(direction=enums.MESSAGE_OUTBOUND, recipient=uuid) | Q(direction=enums.MESSAGE_INBOUND, sender=uuid))

    def for_channel(self, channel):
        return self.filter(channel=channel)

    def for_task(self, task_sid):
        return self.filter(task_sid=task_sid)

    def for_worker(self, worker_sid):
        return self.filter(worker_sid=worker_sid)


class MessageManager(BaseUserManager):
    def get_queryset(self):
        return MessageQuerySet(self.model, using=self._db)

    def inbound(self):
        return self.get_queryset().inbound()

    def not_resolved(self):
        return self.get_queryset().not_resolved()

    def has_task(self):
        return self.get_queryset().has_task()

    def no_worker(self):
        return self.get_queryset().no_worker()

    def for_contact(self, uuid):
        return self.get_queryset().for_contact(uuid)

    def for_channel(self, channel):
        return self.get_queryset().for_channel(channel)

    def for_task(self, task_sid):
        return self.get_queryset().for_task(task_sid)

    def for_worker(self, worker_sid):
        return self.get_queryset().for_worker(worker_sid)
