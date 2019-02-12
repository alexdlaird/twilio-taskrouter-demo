import json
import logging

from rest_framework.views import APIView

from twiltwil.common.utils import viewutils

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"

logger = logging.getLogger(__name__)


class WebhookVoiceConferenceView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info('Voice Conference POST received: {}'.format(json.dumps(request.data)))

        return viewutils.get_empty_voice_webhook_response()
