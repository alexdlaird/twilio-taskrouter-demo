"""
Authentication-based service functions for interacting with Twilio's TaskRouter.
"""
import json
import logging

from django.conf import settings
from twilio.jwt.taskrouter.capabilities import WorkerCapabilityToken
from twilio.rest import Client

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def create_worker(workspace_sid, friendly_name, attributes):
    return client.taskrouter.workspaces(workspace_sid).workers.create(
        friendly_name=friendly_name,
        attributes=json.dumps(attributes)
    )


def delete_worker(workspace_sid, worker_sid):
    client.taskrouter.workspaces(workspace_sid).workers(worker_sid).delete()


def get_worker_token(workspace_sid, worker_sid):
    capability = WorkerCapabilityToken(
        account_sid=settings.TWILIO_ACCOUNT_SID,
        auth_token=settings.TWILIO_AUTH_TOKEN,
        workspace_sid=workspace_sid,
        worker_sid=worker_sid
    )
    capability.allow_update_activities()
    capability.allow_update_reservations()

    return capability.to_jwt()


def get_formatted_number(phone_number):
    number = client.lookups.phone_numbers(phone_number).fetch()

    return number.national_format
