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


def get_or_create_conversation(contact, message):
    try:
        conversation = client.conversations.v1.services(twilioauthservice.get_service().sid).conversations(
            contact.uuid).fetch()

        logger.info(f"Found existing Conversation for {contact.uuid}")
    except TwilioRestException as e:
        if e.status != 404:
            raise e

        logger.info(f"Creating a Conversation for {contact.uuid}")

        conversation = client.conversations.v1.services(twilioauthservice.get_service().sid).conversations.create(
            friendly_name=contact.phone_number,
            unique_name=contact.uuid
        )

        # Since this is a new Conversation, the sender has not been added as a Participant, thus we must
        # manually add the first message
        send_conversation_message(conversation, contact.phone_number, message.text)

    # Ensure Participant is in Conversation
    try:
        client.conversations.v1.services(twilioauthservice.get_service().sid).conversations(
            conversation.sid).participants.create(
            messaging_binding_address=contact.phone_number,
            messaging_binding_proxy_address=settings.TWILIO_PHONE_NUMBER,
        )

        logger.info(f"Added Participant {contact.phone_number} to Conversation {contact.uuid}")
    except TwilioRestException as e:
        if e.code != 50416:
            raise e

        logger.info(f"Participant {contact.phone_number} already added to Conversation {contact.uuid}")

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


def send_conversation_message(conversation, author, message):
    logger.info(f"Sending on Conversation {conversation.unique_name} Message '{message}' from {author}")

    return client.conversations.v1.services(twilioauthservice.get_service().sid).conversations(
        conversation.sid).messages.create(
        body=message,
        author=author
    )
