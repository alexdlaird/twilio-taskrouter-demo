"""
Authentication-based service functions for interacting with Twilio"s TaskRouter.
"""

__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import json
import logging
import os

from django.conf import settings
from django.core.cache import cache
from django.urls import reverse
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant, ChatGrant
from twilio.jwt.client import ClientCapabilityToken
from twilio.jwt.taskrouter.capabilities import WorkerCapabilityToken, WorkspaceCapabilityToken
from twilio.rest import Client

from twiltwil.common import enums

logger = logging.getLogger(__name__)

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, region=settings.TWILIO_REGION)

if settings.TWILIO_REGION and settings.TWILIO_REGION in ["dev", "stage"]:
    head, tail = WorkspaceCapabilityToken.DOMAIN.split(".", 1)
    if not tail.startswith(settings.TWILIO_REGION):
        WorkspaceCapabilityToken.DOMAIN = ".".join([head, settings.TWILIO_REGION, tail])
        WorkerCapabilityToken.DOMAIN = ".".join([head, settings.TWILIO_REGION, tail])
    WorkspaceCapabilityToken.EVENTS_BASE_URL = settings.TWILIO_EVENT_BRIDGE_BASE_URL + "/v1/wschannels"
    WorkerCapabilityToken.EVENTS_BASE_URL = settings.TWILIO_EVENT_BRIDGE_BASE_URL + "/v1/wschannels"

_workspace = None
_activities = {}
_workflow = None
_service = None


def _get_activity(friendly_name):
    return get_activities()[friendly_name]


def _create_service(service_name):
    service = client.conversations.v1.services.create(
        friendly_name=service_name,
    )

    return service


def _create_workspace(workspace_name):
    return client.taskrouter.v1.workspaces.create(
        friendly_name=workspace_name,
        template="EMPTY"
    )


def _create_activities():
    """
    Create the default Activities.
    """
    client.taskrouter.v1.workspaces(get_workspace().sid).activities.create(
        friendly_name="Offline"
    )
    client.taskrouter.v1.workspaces(get_workspace().sid).activities.create(
        friendly_name="Idle",
        available=True
    )
    client.taskrouter.v1.workspaces(get_workspace().sid).activities.create(
        friendly_name="Busy"
    )
    client.taskrouter.v1.workspaces(get_workspace().sid).activities.create(
        friendly_name="Reserved"
    )


def _create_queues():
    """
    Create one Queue per language, plus a default Queue that is a catch all in case the language is not recognized.

    :return: the created default Queues
    """
    queues = {
        "default": client.taskrouter.v1.workspaces(get_workspace().sid).task_queues.create(
            friendly_name="Default",
            reservation_activity_sid=_get_activity("Reserved").sid,
            assignment_activity_sid=_get_activity("Busy").sid,
            target_workers="1==1"
        )
    }

    for language in enums.LANGUAGE_CHOICES:
        queues[language[0]] = client.taskrouter.v1.workspaces(get_workspace().sid).task_queues.create(
            friendly_name=language[1],
            reservation_activity_sid=_get_activity("Reserved").sid,
            assignment_activity_sid=_get_activity("Busy").sid,
            target_workers=f'languages HAS "{language[0]}"'
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
        "task_routing": {
            # Specific filters will be appended below
            "filters": [
            ],
            # If the Task does not match any of the defined filters (below), the default Queue will catch it
            "default_filter": {
                "queue": queues["default"].sid
            }
        }
    }

    for language in enums.LANGUAGE_CHOICES:
        config["task_routing"]["filters"].append(
            {
                # Map a Task to the appropriate Queue based on language, then filter to a Worker with the matching
                # skills, falling back to "default" (above) if no matching is made
                "filter_friendly_name": language[0],
                "expression": f'language=="{language[0]}"',
                "targets": [
                    {
                        "queue": queues[language[0]].sid
                    }
                ]
            }
        )

    return client.taskrouter.v1.workspaces(workspace_sid).workflows.create(
        friendly_name="Default",
        task_reservation_timeout="300",
        configuration=json.dumps(config)
    )


def get_service():
    global _service

    service_name = os.environ.get("TWILTWIL_ID") + "_" + os.environ.get("ENVIRONMENT")

    if not _service:
        for service in client.conversations.v1.services.list():
            if service.friendly_name == service_name:
                _service = service

                break

    if not _service:
        _service = _create_service(service_name)
        update_service_webhooks(_service)

    return _service


def get_workspace():
    global _workspace, _workflow

    workspace_name = os.environ.get("TWILTWIL_ID") + "_" + os.environ.get("ENVIRONMENT")

    if not _workspace:
        for workspace in client.taskrouter.v1.workspaces.list():
            if workspace.friendly_name == workspace_name:
                _workspace = workspace

                break

    if not _workspace:
        _workspace = _create_workspace(workspace_name)
        update_workspace_webhooks(_workspace)

        _create_activities()

        idle_activity_sid = _get_activity("Idle").sid
        client.taskrouter.v1.workspaces(_workspace.sid).update(default_activity_sid=idle_activity_sid,
                                                               timeout_activity_sid=idle_activity_sid)

        queues = _create_queues()

        _workflow = _create_workflow(queues)
        update_workflow_webhooks(_workspace, _workflow)

    return _workspace


def get_workflow():
    global _workflow

    if not _workflow:
        _workflow = client.taskrouter.v1.workspaces(get_workspace().sid).workflows.list()[0]

    return _workflow


def get_activities():
    global _activities

    if len(_activities) == 0:
        for activity in client.taskrouter.v1.workspaces(get_workspace().sid).activities.list():
            _activities[activity.friendly_name] = activity

    return _activities


def create_worker(friendly_name, attributes):
    logger.info(f"Creating Worker {friendly_name} with attributes {attributes}")

    attributes["contact_uri"] = f"client:{friendly_name}"

    return client.taskrouter.v1.workspaces(get_workspace().sid).workers.create(
        friendly_name=friendly_name,
        activity_sid=_get_activity("Idle").sid,
        attributes=json.dumps(attributes)
    )


def delete_worker(worker_sid):
    logger.info(f"Deleting Worker {worker_sid}")

    # Fetch any Tasks associated with the Worker
    for task in client.taskrouter.v1.workspaces(get_workspace().sid).tasks.list():
        logger.info(f"Deleting Task {task.sid}")

        task.delete()

    worker = client.taskrouter.v1.workspaces(get_workspace().sid).workers(worker_sid).fetch()
    worker = worker.update(activity_sid=_get_activity("Offline").sid)
    worker.delete()


def get_chat_token(username):
    logger.info(f"Generating Chat token for {username}")

    # This call is simply to ensure the service exists
    service = get_service()

    token = AccessToken(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_API_KEY, settings.TWILIO_API_SECRET,
                        identity=username)

    sync_grant = SyncGrant(service_sid="default")
    token.add_grant(sync_grant)

    chat_grant = ChatGrant(service_sid=service.sid)
    token.add_grant(chat_grant)

    # Expire token in three minutes
    expiration = 180

    jwt_token = token.to_jwt(ttl=expiration)

    # Cache the token, set to expire after the token expires
    cache.set(f"tokens:chat:{username}", jwt_token, expiration)

    return jwt_token


def get_voice_token(username):
    logger.info(f"Generating Voice token for {username}")

    token = ClientCapabilityToken(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    token.allow_client_incoming(username)

    # Expire token in three minutes
    expiration = 180

    jwt_token = token.to_jwt(ttl=expiration)

    # Cache the token, set to expire after the token expires
    cache.set(f"tokens:voice:{username}", jwt_token, expiration)

    return jwt_token


def get_workspace_token():
    workspace_sid = get_workspace().sid

    logger.info(f"Generating Workspace token for {workspace_sid}")

    token = WorkspaceCapabilityToken(
        account_sid=settings.TWILIO_ACCOUNT_SID,
        auth_token=settings.TWILIO_AUTH_TOKEN,
        workspace_sid=workspace_sid,
    )
    token.allow_fetch_subresources()
    token.allow_update_subresources()
    token.allow_delete_subresources()

    # Expire token in three minutes
    expiration = 180

    jwt_token = token.to_jwt(ttl=expiration)

    # Cache the token, set to expire after the token expires
    cache.set(f"tokens:workspaces:{workspace_sid}", jwt_token, expiration)

    return jwt_token


def get_worker_token(worker_sid):
    logger.info(f"Generating Worker token for {worker_sid}")

    token = WorkerCapabilityToken(
        account_sid=settings.TWILIO_ACCOUNT_SID,
        auth_token=settings.TWILIO_AUTH_TOKEN,
        workspace_sid=get_workspace().sid,
        worker_sid=worker_sid
    )
    token.allow_fetch_subresources()
    token.allow_update_activities()
    token.allow_update_reservations()

    # Expire token in three minutes
    expiration = 180

    jwt_token = token.to_jwt(ttl=expiration)

    # Cache the token, set to expire after the token expires
    cache.set(f"tokens:workers:{worker_sid}", jwt_token, expiration)

    return jwt_token


def get_workers():
    return client.taskrouter.v1.workspaces(get_workspace().sid).workers.list()


def get_worker_by_username(username):
    return client.taskrouter.v1.workspaces(get_workspace().sid).workers.list(friendly_name=username)


def delete_conversation_user(username):
    logger.info(f"Deleting Conversation user {username}")

    service_sid = get_service().sid

    user = client.conversations.v1.services(service_sid).users(username).fetch()
    user.delete()


def update_phone_number_webhooks():
    phone_number = client.incoming_phone_numbers.list(phone_number=settings.TWILIO_PHONE_NUMBER)[0]
    client.incoming_phone_numbers(phone_number.sid).update(
        voice_url=settings.PROJECT_HOST + reverse("api_webhooks_voice"),
        sms_url=settings.PROJECT_HOST + reverse("api_webhooks_sms"))


def update_service_webhooks(service):
    client.conversations.v1.services(service.sid).configuration.webhooks().update(
        post_webhook_url=settings.PROJECT_HOST + reverse("api_webhooks_conversation_event"),
        method="POST",
        filters=["onMessageAdded", "onConversationAdded", "onConversationRemoved"]
    )


def update_workspace_webhooks(workspace):
    client.taskrouter.v1.workspaces(workspace.sid).update(
        event_callback_url=settings.PROJECT_HOST + reverse("api_webhooks_taskrouter_workspace"))


def update_workflow_webhooks(workspace, workflow):
    client.taskrouter.v1.workspaces(workspace.sid).workflows(workflow.sid).update(
        assignment_callback_url=settings.PROJECT_HOST + reverse("api_webhooks_taskrouter_workflow"))
