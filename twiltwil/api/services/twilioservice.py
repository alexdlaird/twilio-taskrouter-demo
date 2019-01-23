"""
Service functions for interacting with Twilio's TaskRouter.
"""
import json
import logging

from django.conf import settings
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from twiltwil.auth.services import twilioauthservice

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.1.0"

logger = logging.getLogger(__name__)

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def get_task(task_sid):
    return client.taskrouter.workspaces(twilioauthservice.get_workspace().sid).tasks(task_sid).fetch()


def create_task(attributes):
    logger.info('Creating a Task with attributes {}'.format(attributes))

    return client.taskrouter.workspaces(twilioauthservice.get_workspace().sid).tasks.create(
        workflow_sid=twilioauthservice.get_workflow().sid,
        attributes=json.dumps(attributes),
        timeout=3600
    )


def cancel_worker_task(username, task_sid):
    logger.info('Canceling/completing Task {}'.format(task_sid))

    client.taskrouter.workspaces(twilioauthservice.get_workspace().sid).tasks(task_sid).update(
        assignment_status='completed',
        reason='User logged out: {}'.format(username)
    )


def get_or_create_channel(number, unique_name):
    try:
        return client.chat.services(twilioauthservice.get_service().sid).channels(unique_name).fetch()
    except TwilioRestException as e:
        if e.status != 404:
            raise e

        logger.info('Creating a Channel for {}'.format(unique_name))

        return client.chat.services(twilioauthservice.get_service().sid).channels.create(
            friendly_name=number,
            unique_name=unique_name
        )


def send_chat_message(channel, message):
    logger.info('Sending on Channel {} a Chat with message {}'.format(channel.unique_name, message))

    return client.chat.services(twilioauthservice.get_service().sid).channels(channel.sid).messages.create(
        body=message.text,
        from_=message.sender
    )


def send_sms(phone, message):
    logger.info('Sending SMS message {} to {}'.format(message, phone))

    client.api.account.messages.create(
        to=phone,
        from_=settings.TWILIO_SMS_FROM,
        body=message)
