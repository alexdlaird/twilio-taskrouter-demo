import json
import logging

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from twiltwil.api.models import Message
from twiltwil.common import enums

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)


class WebhookSmsView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info('SMS POST received: {}'.format(json.dumps(request.data)))

        Message.objects.update_or_create(sid=request.data['SmsSid'], defaults={
            "sender": request.data['From'],
            "receiver": request.data['To'],
            "direction": enums.MESSAGE_INBOUND if request.data['To'] == settings.TWILTWIL_TWILIO_SMS_FROM else enums.MESSAGE_OUTBOUND,
            "status": request.data['SmsStatus'],
            "text": request.data['Body'],
            "addons": json.dumps(request.data['AddOns']) if 'AddOns' in request.data else None,
            "raw": json.dumps(request.data),
        })

        return Response()
