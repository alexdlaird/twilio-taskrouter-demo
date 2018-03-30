import json
import logging

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)


class WebhookMessengerView(APIView):
    def get(self, request, *args, **kwargs):
        token_sent = request.GET.get("hub.verify_token")

        if token_sent == settings.MESSENGER_VERIFY_TOKEN:
            return request.GET.get("hub.challenge")

        return 'Invalid verification token'

    def post(self, request, *args, **kwargs):
        logger.info('Messenger POST received: {}'.format(json.dumps(request.data)))

        return Response()
