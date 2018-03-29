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


class WebhookSmsView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info('SMS POST received: {}'.format(json.dumps(request.data)))

        # Store (or update, if this message is redundant) the message in the database
        message, created = Message.objects.update_or_create(sid=request.data['SmsSid'], defaults={
            "channel": enums.CHANNEL_SMS,
            "sender": request.data['From'],
            "receiver": request.data['To'],
            "direction": enums.MESSAGE_INBOUND,
            "status": request.data['SmsStatus'],
            "text": request.data['Body'],
            "addons": messageutils.cleanup_json(request.data['AddOns']) if 'AddOns' in request.data else None,
            "raw": json.dumps(request.data),
        })

        # Check if the other messages exist from this sender that are associated with an open Task
        sender_messages_with_tasks = Message.objects.inbound().for_number(request.data['From']).has_task()
        task = None
        if sender_messages_with_tasks.exists():
            task = twilioservice.get_task(sender_messages_with_tasks[0].task_sid)

            if task.assignment_status not in ['reserved', 'assigned']:
                task = None

        # If no open Task was found, create a new one
        if not task:
            attributes = {
                "from": message.sender
            }

            message_addons = json.loads(message.addons)
            if message_addons and \
                            "ibm_watson_insights" in message_addons and \
                            "result" in message_addons["ibm_watson_insights"] and \
                            "language" in message_addons["ibm_watson_insights"]["result"]:
                attributes["language"] = message_addons["ibm_watson_insights"]["result"]["language"]

            attributes["skill"] = enums.GENERAL

            task = twilioservice.create_task(attributes)

        # TODO: send message to Worker with Task

        return Response()
