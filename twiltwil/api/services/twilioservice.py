"""
Service functions for interacting with Twilio's APIs.
"""
import json
import logging

from django.conf import settings
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from twiltwil.auth.services import twilioauthservice

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.1"

logger = logging.getLogger(__name__)

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, region=settings.TWILIO_REGION)


def get_task(task_sid):
    return client.taskrouter.workspaces(twilioauthservice.get_workspace().sid).tasks(task_sid).fetch()


def create_task(attributes):
    logger.info(f'Creating a Task with attributes {attributes}')

    return client.taskrouter.workspaces(twilioauthservice.get_workspace().sid).tasks.create(
        workflow_sid=twilioauthservice.get_workflow().sid,
        attributes=json.dumps(attributes),
        timeout=3600
    )


def complete_task(task_sid, reason=''):
    logger.info(f'Canceling/completing Task {task_sid}')

    client.taskrouter.workspaces(twilioauthservice.get_workspace().sid).tasks(task_sid).update(
        assignment_status='completed',
        reason=reason
    )


def get_or_create_chat_channel(number, unique_name):
    try:
        return client.chat.services(twilioauthservice.get_service().sid).channels(unique_name).fetch()
    except TwilioRestException as e:
        if e.status != 404:
            raise e

        logger.info(f'Creating a Channel for {unique_name}')

        return client.chat.services(twilioauthservice.get_service().sid).channels.create(
            friendly_name=number,
            unique_name=unique_name
        )


def send_chat_message(channel, message):
    logger.info(f'Sending on Channel {channel.unique_name} a Chat with message {message}')

    return client.chat.services(twilioauthservice.get_service().sid).channels(channel.sid).messages.create(
        body=message.text,
        from_=message.sender
    )


def send_sms(phone, message):
    logger.info(f'Sending SMS message {message} to {phone}')

    client.api.account.messages.create(
        to=phone,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=message)
