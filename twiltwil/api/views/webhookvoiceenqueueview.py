__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import json
import logging
import uuid

from django.http import HttpResponse
from django.utils import timezone
from rest_framework.views import APIView
from twilio.twiml.voice_response import VoiceResponse

from twiltwil.api.models import Contact, Message
from twiltwil.api.services import twilioservice
from twiltwil.api.utils import messageutils
from twiltwil.auth.services import twilioauthservice
from twiltwil.common import enums

logger = logging.getLogger(__name__)


class WebhookVoiceEnqueueView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info(f"Voice Enqueue POST received: {json.dumps(request.data)}")

        digit_pressed = int(request.data.get("Digits", "1"))
        if digit_pressed == 1:
            language = "english"
        else:
            language = "spanish"

        # Store (or update, if this redundant) the contact and message in the database
        contact, created = Contact.objects.get_or_create(phone_number=request.data["From"], defaults={
            "uuid": uuid.uuid4(),
            "phone_number": request.data["From"],
        })

        Message.objects.update_or_create(sid=request.data["CallSid"], defaults={
            "timestamp": timezone.now(),
            "channel": enums.CHANNEL_VOICE,
            "sender": contact.uuid,
            "recipient": request.data["To"],
            "direction": enums.MESSAGE_INBOUND,
            "status": request.data["CallStatus"],
            "addons": messageutils.cleanup_json(request.data["AddOns"]) if "AddOns" in request.data else None,
            "raw": json.dumps(request.data),
        })

        conversation = twilioservice.get_or_create_conversation(contact.phone_number, str(contact.uuid))

        attributes = {
            "from": str(contact.uuid),
            "language": language,
            "conversation": conversation.unique_name
        }

        response = VoiceResponse()
        enqueue = response.enqueue(None, workflow_sid=twilioauthservice.get_workflow().sid)
        enqueue.task(json.dumps(attributes))
        response.append(enqueue)

        return HttpResponse(str(response))
