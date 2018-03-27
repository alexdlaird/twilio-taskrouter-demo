"""
Authentication-based service functions for interacting with Twilio's TaskRouter.
"""
import json
import logging
import os

from django.conf import settings
from django.urls import reverse
from twilio.jwt.taskrouter.capabilities import WorkerCapabilityToken
from twilio.rest import Client

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

# TODO: refactor to use a class instead of globals
_workspace = None
_activities = []
_offline_activity = None
_idle_activity = None


def _get_offline_activity():
    global _offline_activity

    if not _offline_activity:
        for activity in get_activities():
            if activity.friendly_name == 'Offline':
                _offline_activity = activity

                break

    return _offline_activity


def _get_idle_activity():
    global _idle_activity

    if not _idle_activity:
        for activity in get_activities():
            if activity.friendly_name == 'Idle':
                _idle_activity = activity

                break

    return _idle_activity


def _create_workspace(workspace_name):
    workspace = client.taskrouter.workspaces.create(
        friendly_name=workspace_name,
        event_callback_url=settings.PROJECT_HOST + reverse('api_webhook_taskrouter_workspace'),
    )

    # TODO: create FIFO Queues here, one for each expression to match

    # TODO: create Workflows for Queues here

    return workspace


def get_workspace():
    global _workspace

    workspace_name = 'twiltwil_' + os.environ.get('ENVIRONMENT')

    if not _workspace:
        for workspace in client.taskrouter.workspaces.list():
            if workspace.friendly_name == workspace_name:
                _workspace = workspace

                break

    if not _workspace:
        _workspace = _create_workspace(workspace_name)

    return _workspace


def get_activities():
    global _activities

    if len(_activities) == 0:
        _activities = client.taskrouter.workspaces(get_workspace().sid).activities.list()

    return _activities


def create_worker(friendly_name, attributes):
    return client.taskrouter.workspaces(get_workspace().sid).workers.create(
        friendly_name=friendly_name,
        activity_sid=_get_idle_activity().sid,
        attributes=json.dumps(attributes)
    )


def delete_worker(worker_sid):
    worker = client.taskrouter.workspaces(get_workspace().sid).workers(worker_sid).fetch()
    worker = worker.update(activity_sid=_get_offline_activity().sid)
    worker.delete()


def get_worker_token(worker_sid):
    capability = WorkerCapabilityToken(
        account_sid=settings.TWILIO_ACCOUNT_SID,
        auth_token=settings.TWILIO_AUTH_TOKEN,
        workspace_sid=get_workspace().sid,
        worker_sid=worker_sid
    )
    capability.allow_update_activities()
    capability.allow_update_reservations()

    return capability.to_jwt()
