__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import json
import logging

from dateutil import parser
from django.conf import settings
from rest_framework.views import APIView

from twiltwil.api.models import Contact, Message
from twiltwil.api.services import twilioservice
from twiltwil.api.utils import messageutils
from twiltwil.common import enums
from twiltwil.common.utils import viewutils

logger = logging.getLogger(__name__)


class WebhookChatEventView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info(f'Chat POST received: {json.dumps(request.data)}')

        if 'EventType' in request.data:
            if request.data['EventType'] == 'onMessageSent':
                logger.info('Processing onMessageSent')

                attributes = json.loads(messageutils.cleanup_json(request.data['Attributes']))

                # TODO: detect the originating channel of the inbound (ex. SMS)
                channel = enums.CHANNEL_SMS
                contact = Contact.objects.get(uuid=attributes['To'])

                # TODO: here you would execute different "sends" for different originating channels
                if channel == enums.CHANNEL_SMS:
                    twilioservice.send_sms(contact.phone_number,
                                           f"{request.data['Body']} - {request.data['ClientIdentity']}")

                # Store (or update, if this message is redundant) the message in the database
                Message.objects.update_or_create(sid=request.data['MessageSid'], defaults={
                    "timestamp": parser.parse(request.data['DateCreated']),
                    "channel": channel,
                    "sender": settings.TWILIO_PHONE_NUMBER,
                    "recipient": contact.uuid,
                    "direction": enums.MESSAGE_OUTBOUND,
                    "status": enums.MESSAGE_STATUS_SENT,
                    "text": request.data['Body'],
                    "raw": json.dumps(request.data),
                })

        return viewutils.get_empty_messaging_webhook_response()
