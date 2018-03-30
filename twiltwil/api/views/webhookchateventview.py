import json
import logging

from django.conf import settings
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


class WebhookChatEventView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info('Chat POST received: {}'.format(json.dumps(request.data)))

        if 'EventType' in request.data:
            if request.data['EventType'] == 'onMessageSent':
                logger.info('Processing onMessageSent')

                # TODO: lookup what the last inbound Message type was for this Channel, then send on that type (ex. SMS)

                attributes = json.loads(messageutils.cleanup_json(request.data['Attributes']))
                twilioservice.send_sms(attributes['To'],
                                       '{} - {}'.format(request.data['Body'], request.data['ClientIdentity']))

                # Store (or update, if this message is redundant) the message in the database
                Message.objects.update_or_create(sid=request.data['MessageSid'], defaults={
                    "channel": enums.CHANNEL_SMS,
                    "sender": settings.TWILIO_SMS_FROM,
                    "receiver": attributes['To'],
                    "direction": enums.MESSAGE_OUTBOUND,
                    "status": enums.MESSAGE_STATUS_SENT,
                    "text": request.data['Body'],
                    "raw": json.dumps(request.data),
                })

        return Response()
