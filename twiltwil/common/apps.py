__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import os
import sys
from urllib.parse import urlparse

from django.apps import AppConfig
from django.conf import settings
from django.urls import reverse
from twilio.rest import Client


class CommonConfig(AppConfig):
    name = "twiltwil.common"
    verbose_name = "Common"

    def ready(self):
        if settings.USE_NGROK and os.environ.get("NGROK_AUTHTOKEN"):
            # pyngrok will only be installed, and should only ever be initialized, in a dev environment
            from pyngrok import ngrok

            # Get the dev server port (defaults to 8000 for Django, can be overridden with the
            # last arg when calling `runserver`)
            addrport = urlparse(f"http://{sys.argv[-1]}")
            port = addrport.port if addrport.netloc and addrport.port else 8000

            # Open a ngrok tunnel to the dev server
            public_url = ngrok.connect(port).public_url
            print(f"ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{port}\"")

            # Update any base URLs or webhooks to use the public ngrok URL
            CommonConfig.init_webhooks(public_url)

    @staticmethod
    def init_webhooks(public_url):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, region=settings.TWILIO_REGION)

        phone_number = client.incoming_phone_numbers.list(phone_number=settings.TWILIO_PHONE_NUMBER)[0]
        client.incoming_phone_numbers(phone_number.sid).update(voice_url=f"{public_url}/api/webhooks/voice",
                                                               sms_url=f"{public_url}/api/webhooks/sms")

        resource_name = "twiltwil_" + os.environ.get("ENVIRONMENT")

        for service in client.conversations.v1.services.list():
            if service.friendly_name == resource_name:
                client.conversations.v1.services(service.sid).configuration.webhooks().update(
                    post_webhook_url=f"{public_url}/api/webhooks/chat/event",
                    method="POST",
                    filters=["onMessageAdded", "onConversationAdded", "onConversationRemoved"]
                )

        workspaces = client.taskrouter.v1.workspaces.list(friendly_name=resource_name)
        if len(workspaces) > 0:
            client.taskrouter.v1.workspaces(workspaces[0].sid).update(
                event_callback_url=f"{public_url}/api/webhooks/taskrouter/workspace")

            for workflow in client.taskrouter.v1.workspaces(workspaces[0].sid).workflows.list():
                client.taskrouter.v1.workspaces(workspaces[0].sid).workflows(workflow.sid).update(
                    assignment_callback_url=f"{public_url}/api/webhooks/taskrouter/workflow")
