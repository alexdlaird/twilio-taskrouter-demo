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


def _get_offline_activity(workspace_sid):
    # TODO: cache this
    for activity in client.taskrouter.workspaces(workspace_sid).activities.list():
        if activity.friendly_name == 'Offline':
            return activity


def create_worker(workspace_sid, friendly_name, attributes):
    return client.taskrouter.workspaces(workspace_sid).workers.create(
        friendly_name=friendly_name,
        attributes=json.dumps(attributes)
    )


def delete_worker(workspace_sid, worker_sid):
    worker = client.taskrouter.workspaces(workspace_sid).workers(worker_sid).fetch()
    worker = worker.update(activity_sid=_get_offline_activity(workspace_sid).sid)
    worker.delete()


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
