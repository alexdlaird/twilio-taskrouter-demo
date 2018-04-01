import json
import logging

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from twiltwil.api.models import Message, Contact
from twiltwil.api.services import twilioservice
from twiltwil.api.utils import messageutils
from twiltwil.common import enums

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)


class WebhookTaskRouterWorkspaceView(APIView):
    def _cancel_task(self, attributes):
        # TODO: we're just cancelling the Task here (TaskRouter doesn't support automatic reassignment), but a more robust solution would be to simply create a new Task for requeuing
        task_attributes = json.loads(messageutils.cleanup_json(attributes))

        # TODO: detect the originating channel of the inbound (ex. SMS)
        channel = enums.CHANNEL_SMS
        contact = Contact.objects.get(sid=task_attributes['from'])

        # TODO: here you would execute different "sends" for different originating channels
        if channel == enums.CHANNEL_SMS:
            twilioservice.send_sms(contact.phone_number, settings.CANCELLED_MESSAGE)

    def post(self, request, *args, **kwargs):
        logger.info('Workspace POST received: {}'.format(json.dumps(request.data)))

        if 'EventType' in request.data:
            if request.data['EventType'] == 'reservation.accepted':
                logger.info('Processing reservation.accepted')

                task_attributes = json.loads(messageutils.cleanup_json(request.data['TaskAttributes']))

                for message in Message.objects.not_resolved().for_channel('sms').inbound().for_contact(
                        task_attributes['from']).no_worker().iterator():
                    message.worker_sid = request.data['WorkerSid']

                    message.save()
            elif request.data['EventType'] == 'task.created':
                logger.info('Processing task.created')

                task_attributes = json.loads(messageutils.cleanup_json(request.data['TaskAttributes']))

                for message in Message.objects.not_resolved().for_channel('sms').inbound().for_contact(
                        task_attributes['from']).no_worker().iterator():
                    message.task_sid = request.data['TaskSid']

                    message.save()
            elif request.data['EventType'] == 'task.canceled':
                logger.info('Processing task.canceled')

                self._cancel_task(request.data['TaskAttributes'])
            elif request.data['EventType'] == 'task.completed':
                logger.info('Processing task.completed')

                if 'TaskCompletedReason' in request.data and request.data['TaskCompletedReason'].startswith(
                        'User logged out'):
                    self._cancel_task(request.data['TaskAttributes'])

                for message in Message.objects.for_task(request.data['TaskSid']).iterator():
                    message.worker_sid = None
                    message.resolved = True
                    message.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
