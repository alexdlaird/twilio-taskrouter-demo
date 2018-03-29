"""
Service functions for interacting with Twilio's TaskRouter.
"""
import json
import logging

from django.conf import settings
from twilio.rest import Client

from twiltwil.auth.services import twilioauthservice

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def get_task(task_sid):
    return client.taskrouter.workspaces(twilioauthservice.get_workspace().sid).tasks(task_sid).fetch()


def create_task(attributes):
    return client.taskrouter.workspaces(twilioauthservice.get_workspace().sid).tasks.create(
        workflow_sid=twilioauthservice.get_workflow().sid,
        attributes=json.dumps(attributes)
    )
