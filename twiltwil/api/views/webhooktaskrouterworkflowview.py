import json
import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from twiltwil.api.models import Message
from twiltwil.api.utils import messageutils

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)


class WebhookTaskRouterWorkflowView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info('Workflow POST received: {}'.format(json.dumps(request.data)))

        if 'EventType' in request.data:
            if request.data['EventType'] == 'reservation.accepted':
                logger.info('Processing reservation.accepted')

                task_attributes = json.loads(messageutils.cleanup_json(request.data['TaskAttributes']))

                for message in Message.objects.for_channel('sms').inbound().for_number(
                        task_attributes['from']).no_worker().iterator():
                    message.task_sid = request.data['TaskSid']
                    message.worker_sid = request.data['WorkerSid']

                    message.save()

        return Response()
