__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import json
import logging

from rest_framework.views import APIView

from twiltwil.common.utils import viewutils

logger = logging.getLogger(__name__)


class WebhookVoiceConferenceView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info(f"Voice Conference POST received: {json.dumps(request.data)}")

        return viewutils.get_empty_voice_webhook_response()
