import json
import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from twiltwil.api.services import twilioservice
from twiltwil.api.utils import messageutils

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)


class WebhookChatEventView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info('Chat POST received: {}'.format(json.dumps(request.data)))

        if 'EventType' in request.data:
            if request.data['EventType'] == 'onMessageSent':
                # TODO: add a check to see if this outbound should be an SMS

                attributes = json.loads(messageutils.cleanup_json(request.data['Attributes']))
                twilioservice.send_sms(attributes['To'], request.data['Body'])

                # TODO: add outbound to "Messages" table

        return Response()
