"""
Service functions for interacting with Twilio"s APIs.
"""

__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import json
import logging

from django.conf import settings
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from twiltwil.auth.services import twilioauthservice

logger = logging.getLogger(__name__)

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, region=settings.TWILIO_REGION)


def get_task(task_sid):
    return client.taskrouter.v1.workspaces(twilioauthservice.get_workspace().sid).tasks(task_sid).fetch()


def create_task(attributes):
    logger.info(f"Creating a Task with attributes {attributes}")

    return client.taskrouter.v1.workspaces(twilioauthservice.get_workspace().sid).tasks.create(
        workflow_sid=twilioauthservice.get_workflow().sid,
        attributes=json.dumps(attributes),
        timeout=3600
    )


def complete_task(task_sid, reason=""):
    logger.info(f"Canceling/completing Task {task_sid}")

    client.taskrouter.v1.workspaces(twilioauthservice.get_workspace().sid).tasks(task_sid).update(
        assignment_status="completed",
        reason=reason
    )


def get_or_create_conversation(number, unique_name):
    try:
        conversation = client.conversations.v1.services(twilioauthservice.get_service().sid).conversations(
            unique_name).fetch()

        logger.info(f"Found existing Conversation for {unique_name}")
    except TwilioRestException as e:
        if e.status != 404:
            raise e

        logger.info(f"Creating a Conversation for {unique_name}")

        conversation = client.conversations.v1.services(twilioauthservice.get_service().sid).conversations.create(
            friendly_name=number,
            unique_name=unique_name
        )

    # Ensure Participant is in Conversation
    try:
        client.conversations.v1.services(twilioauthservice.get_service().sid).conversations(
            conversation.sid).participants.create(
            messaging_binding_address=number,
            messaging_binding_proxy_address=settings.TWILIO_PHONE_NUMBER,
        )

        logger.info(f"Added Participant {number} to Conversation {unique_name}")
    except TwilioRestException as e:
        if e.code != 50416:
            raise e

        logger.info(f"Participant {number} already added to Conversation {unique_name}")

    return conversation


def get_conversation(unique_name):
    return client.conversations.v1.services(twilioauthservice.get_service().sid).conversations(unique_name).fetch()


def add_worker_to_conversation(conversation, identity):
    try:
        client.conversations.v1.services(twilioauthservice.get_service().sid).conversations(
            conversation.sid).participants.create(
            identity=identity
        )

        logger.info(f"Added Participant {identity} to Conversation {conversation.unique_name}")
    except TwilioRestException as e:
        if e.code != 50433:
            raise e

        logger.info(f"Participant {identity} already added to Conversation {conversation.unique_name}")


def send_sms(phone, message):
    logger.info(f"Sending SMS message {message} to {phone}")

    client.api.account.messages.create(
        to=phone,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=message)
