import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete
from django.dispatch import receiver

from twiltwil.auth.services import twilioauthservice

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)


@receiver(post_delete, sender=get_user_model())
def delete_user(sender, instance, **kwargs):
    if not instance.is_superuser:
        twilioauthservice.delete_worker(instance.workspace_sid, instance.worker_sid)
