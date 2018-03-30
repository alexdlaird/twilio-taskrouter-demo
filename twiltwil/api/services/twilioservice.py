"""
Service functions for interacting with Twilio's TaskRouter.
"""
import json
import logging

from django.conf import settings
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from twiltwil.auth.services import twilioauthservice

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def get_task(task_sid):
    return client.taskrouter.workspaces(twilioauthservice.get_workspace().sid).tasks(task_sid).fetch()


def create_task(attributes):
    return client.taskrouter.workspaces(twilioauthservice.get_workspace().sid).tasks.create(
        workflow_sid=twilioauthservice.get_workflow().sid,
        attributes=json.dumps(attributes),
        timeout=3600
    )


def reject_worker_reservations(worker_sid, task_sids):
    workspace_sid = twilioauthservice.get_workspace().sid

    for task_sid in task_sids:
        for reservation in client.taskrouter.workspaces(workspace_sid).tasks(task_sid).reservations.list(
                worker_sid=worker_sid,
                reservation_status='assigned'
        ):
            client.taskrouter.workspaces(workspace_sid).tasks(task_sid).reservations(reservation.sid).update(
                reservation_status='rejected'
            )


def get_or_create_channel(number, unique_name):
    try:
        return client.chat.services(twilioauthservice.get_service().sid).channels(unique_name).fetch()
    except TwilioRestException as e:
        if e.status != 404:
            raise e

        return client.chat.services(twilioauthservice.get_service().sid).channels.create(
            friendly_name=number,
            unique_name=unique_name
        )


def send_chat_message(channel, message):
    return client.chat.services(twilioauthservice.get_service().sid).channels(channel.sid).messages.create(
        body=message.text,
        from_=message.sender
    )


def send_sms(phone, message):
    client.api.account.messages.create(
        to=phone,
        from_=settings.TWILIO_SMS_FROM,
        body=message)
