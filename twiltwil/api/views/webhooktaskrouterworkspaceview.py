import json
import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from twiltwil.api.models import Message
from twiltwil.api.services import twilioservice
from twiltwil.api.utils import messageutils
from twiltwil.common import enums

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)


class WebhookTaskRouterWorkspaceView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info('Workspace POST received: {}'.format(json.dumps(request.data)))

        if 'EventType' in request.data:
            if request.data['EventType'] == 'reservation.accepted':
                logger.info('Processing reservation.accepted')

                task_attributes = json.loads(messageutils.cleanup_json(request.data['TaskAttributes']))

                for message in Message.objects.not_resolved().for_channel('sms').inbound().for_number(
                        task_attributes['from']).no_worker().iterator():
                    message.worker_sid = request.data['WorkerSid']

                    message.save()
            elif request.data['EventType'] == 'task.created':
                logger.info('Processing task.created')

                task_attributes = json.loads(messageutils.cleanup_json(request.data['TaskAttributes']))

                for message in Message.objects.not_resolved().for_channel('sms').inbound().for_number(
                        task_attributes['from']).no_worker().iterator():
                    message.task_sid = request.data['TaskSid']

                    message.save()
            elif request.data['EventType'] == 'task.canceled':
                logger.info('Processing task.canceled')

                task_attributes = json.loads(messageutils.cleanup_json(request.data['TaskAttributes']))

                # TODO: detect the originating channel of the inbound message (ex. SMS)
                channel = enums.CHANNEL_SMS

                # TODO: here you would execute different "sends" for different originating channels
                cancelled_message = 'Sorry, your question could not be answered, probably because an agent was not ' \
                                    'available to take it in a reasonable amount of time. Try again later!'
                if channel == enums.CHANNEL_SMS:
                    twilioservice.send_sms(task_attributes['from'], cancelled_message)
            elif request.data['EventType'] == 'task.completed':
                logger.info('Processing task.completed')

                # TODO: this is a bit of a hack simply because TaskRouter does not support Task reassignment
                if request.data['TaskCompletedReason'].startswith('User logged out'):
                    task_attributes = json.loads(messageutils.cleanup_json(request.data['TaskAttributes']))

                    # TODO: detect the originating channel of the inbound message (ex. SMS)
                    channel = enums.CHANNEL_SMS

                    # TODO: here you would execute different "sends" for different originating channels
                    cancelled_message = 'Sorry, your question could not be answered because the agent assigned to it ' \
                                        'logged out and another agent was not available. Try again later!'
                    if channel == enums.CHANNEL_SMS:
                        twilioservice.send_sms(task_attributes['from'], cancelled_message)

                for message in Message.objects.for_task(request.data['TaskSid']).iterator():
                    message.resolved = True
                    message.save()

        return Response()
