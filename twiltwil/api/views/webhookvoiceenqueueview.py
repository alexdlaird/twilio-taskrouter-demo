import json
import logging

from django.http import HttpResponse
from rest_framework.views import APIView
from twilio.twiml.voice_response import VoiceResponse

from twiltwil.api.models import Contact
from twiltwil.api.services import twilioservice
from twiltwil.auth.services import twilioauthservice

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.1.0"

logger = logging.getLogger(__name__)


class WebhookVoiceEnqueueView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info('Voice Enqueue POST received: {}'.format(json.dumps(request.data)))

        digit_pressed = request.data.get("Digits", 1)
        if digit_pressed == 1:
            language = "en"
        else:
            language = "es"

        # Store (or update, if this redundant) the contact and message in the database
        contact, created = Contact.objects.get_or_create(phone_number=request.data['From'], defaults={
            "uuid": request.data['CallSid'],
            "phone_number": request.data['From'],
        })

        channel = twilioservice.get_or_create_chat_channel(contact.phone_number, str(contact.uuid))

        attributes = {
            "from": str(contact.uuid),
            "language": language,
            "channel": channel.unique_name
        }

        response = VoiceResponse()
        enqueue = response.enqueue(None, workflow_sid=twilioauthservice.get_workflow().sid)
        enqueue.task(json.dumps(attributes))
        response.append(enqueue)

        return HttpResponse(str(response))
