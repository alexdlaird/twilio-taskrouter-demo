__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import json
import logging

from django.http import HttpResponse
from django.urls import reverse
from rest_framework.views import APIView
from twilio.twiml.voice_response import VoiceResponse, Gather

logger = logging.getLogger(__name__)


class WebhookVoiceView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info(f"Voice POST received: {json.dumps(request.data)}")

        response = VoiceResponse()
        gather = Gather(num_digits=1, action=reverse("api_webhooks_voice_enqueue"), method="POST", timeout=5)
        gather.say("For English, please hold or press one.", language="en")
        gather.say("Para Español oprime dos.", language="es")
        response.append(gather)
        response.redirect(reverse("api_webhooks_voice_enqueue"))

        return HttpResponse(str(response))
