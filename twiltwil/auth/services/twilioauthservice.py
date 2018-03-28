"""
Authentication-based service functions for interacting with Twilio's TaskRouter.
"""
import json
import logging
import os

from django.conf import settings
from django.core.cache import cache
from django.urls import reverse
from twilio.jwt.taskrouter.capabilities import WorkerCapabilityToken
from twilio.rest import Client

from twiltwil.common import enums

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

# TODO: refactor to use a class instead of globals
_workspace = None
_activities = {}
_queues = {}


def _get_activity(friendly_name):
    return get_activities()[friendly_name]


def _create_workspace(workspace_name):
    workspace = client.taskrouter.workspaces.create(
        friendly_name=workspace_name,
        event_callback_url=settings.PROJECT_HOST + reverse('api_webhooks_taskrouter_workspace'),
    )

    return workspace


def _create_queues():
    queues = {
        "default": client.taskrouter.workspaces(get_workspace().sid).task_queues.create(
            friendly_name="Default",
            reservation_activity_sid=_get_activity("Reserved").sid,
            assignment_activity_sid=_get_activity("Busy").sid,
            target_workers="1==1"
        )
    }

    for language in enums.LANGUAGE_CHOICES:
        queues[language[0]] = client.taskrouter.workspaces(get_workspace().sid).task_queues.create(
            friendly_name=language[1],
            reservation_activity_sid=_get_activity("Reserved").sid,
            assignment_activity_sid=_get_activity("Busy").sid,
            target_workers='languages HAS "{}"'.format(language[0])
        )

    return queues


def _create_workflows():
    workspace_sid = get_workspace().sid

    config = {
        'task_routing': {
            'filters': [
            ],
            'default_filter': {
                'queue': _queues['default'].sid
            }
        }
    }

    for language in enums.LANGUAGE_CHOICES:
        config['task_routing']['filters'].append(
            {
                'expression': "type=='{}'".format(language[0]),
                'targets': [
                    {
                        'queue': _queues[language[0]].sid,
                        'expression': 'worker.skills HAS task.skill'
                    }
                ]
            }
        )

    client.taskrouter.workspaces(workspace_sid).workflows.create(
        friendly_name='Default',
        assignment_callback_url=settings.PROJECT_HOST + reverse('api_webhooks_taskrouter_workflow'),
        task_reservation_timeout='300',
        configuration=json.dumps(config)
    )


def get_workspace():
    global _workspace, _queues

    workspace_name = 'twiltwil_' + os.environ.get('ENVIRONMENT')

    if not _workspace:
        for workspace in client.taskrouter.workspaces.list():
            if workspace.friendly_name == workspace_name:
                _workspace = workspace

                break

    if not _workspace:
        _workspace = _create_workspace(workspace_name)

        _queues = _create_queues()

        _create_workflows()

    return _workspace


def get_activities():
    global _activities

    if len(_activities) == 0:
        for activity in client.taskrouter.workspaces(get_workspace().sid).activities.list():
            _activities[activity.friendly_name] = activity

    return _activities


def create_worker(friendly_name, attributes):
    return client.taskrouter.workspaces(get_workspace().sid).workers.create(
        friendly_name=friendly_name,
        activity_sid=_get_activity("Idle").sid,
        attributes=json.dumps(attributes)
    )


def delete_worker(worker_sid):
    worker = client.taskrouter.workspaces(get_workspace().sid).workers(worker_sid).fetch()
    worker = worker.update(activity_sid=_get_activity("Offline").sid)
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

    expiration = 3600

    token = capability.to_jwt(ttl=expiration)

    # Cache the token, set to expire when the token expires
    cache.set('tokens:{}'.format(worker_sid), token, expiration)

    return token


def get_workers():
    return client.taskrouter.workspaces(get_workspace().sid).workers.list()
