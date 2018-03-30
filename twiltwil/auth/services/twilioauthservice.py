"""
Authentication-based service functions for interacting with Twilio's TaskRouter.
"""
import json
import logging
import os

from django.conf import settings
from django.core.cache import cache
from django.urls import reverse
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant, ChatGrant
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
_workflow = None
_service = None


def _get_activity(friendly_name):
    return get_activities()[friendly_name]


def _create_service(service_name):
    service = client.chat.services.create(
        friendly_name=service_name,
    )

    service = client.chat.services(service.sid).update(
        post_webhook_url=settings.PROJECT_HOST + reverse('api_webhooks_chat_event'),
        webhook_method='POST',
        webhook_filters=['onMessageSent', 'onChannelAdded', 'onChannelDestroyed']
    )

    return service


def _create_workspace(workspace_name):
    return client.taskrouter.workspaces.create(
        friendly_name=workspace_name,
        event_callback_url=settings.PROJECT_HOST + reverse('api_webhooks_taskrouter_workspace'),
    )


def _create_queues():
    """
    Create one Queue per language, plus a default Queue that is a catch all in case the language is not recognized.

    :return: the created default Queues
    """
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


def _create_workflow(queues):
    """
    Create a workflow that defines rules for filtering tasks to the appropriate Worker based on language and skills.

    :type queues: the language queues for the Workflow
    :return: the created default Workflow
    """
    workspace_sid = get_workspace().sid

    config = {
        'task_routing': {
            # Specific filters will be appended below
            'filters': [
            ],
            # If the Task does not match any of the defined filters (below), the default Queue will catch it
            'default_filter': {
                'queue': queues['default'].sid
            }
        }
    }

    for language in enums.LANGUAGE_CHOICES:
        config['task_routing']['filters'].append(
            {
                # Map a Task to the appropriate Queue based on language, then filter to a Worker with the matching
                # skills, falling back to "default" (above) if no matching is made
                "filter_friendly_name": language[0],
                'expression': "language=='{}'".format(language[0]),
                'targets': [
                    {
                        'queue': queues[language[0]].sid,
                        'expression': 'worker.skills HAS task.skill'
                    }
                ]
            }
        )

    return client.taskrouter.workspaces(workspace_sid).workflows.create(
        friendly_name='Default',
        assignment_callback_url=settings.PROJECT_HOST + reverse('api_webhooks_taskrouter_workflow'),
        task_reservation_timeout='300',
        configuration=json.dumps(config)
    )


def get_service():
    global _service

    service_name = 'twiltwil_' + os.environ.get('ENVIRONMENT')

    if not _service:
        for service in client.chat.services.list():
            if service.friendly_name == service_name:
                _service = service

                break

    if not _service:
        _service = _create_service(service_name)

    return _service


def get_workspace():
    global _workspace, _workflow

    workspace_name = 'twiltwil_' + os.environ.get('ENVIRONMENT')

    if not _workspace:
        for workspace in client.taskrouter.workspaces.list():
            if workspace.friendly_name == workspace_name:
                _workspace = workspace

                break

    if not _workspace:
        _workspace = _create_workspace(workspace_name)

        queues = _create_queues()

        _workflow = _create_workflow(queues)

    return _workspace


def get_workflow():
    global _workflow

    if not _workflow:
        _workflow = client.taskrouter.workspaces(get_workspace().sid).workflows.list()[0]

    return _workflow


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


def get_chat_token(username):
    # This call is simply to ensure the service exists, though it is not needed to generate token
    service = get_service()

    token = AccessToken(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_API_KEY, settings.TWILIO_API_SECRET,
                        identity=username)

    sync_grant = SyncGrant(service_sid='default')
    token.add_grant(sync_grant)

    chat_grant = ChatGrant(service_sid=service.sid)
    token.add_grant(chat_grant)

    return token.to_jwt()


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
