import os
import sys
from urllib.parse import urlparse

from django.apps import AppConfig
from django.conf import settings
from twilio.rest import Client

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.3"


class CommonConfig(AppConfig):
    name = 'twiltwil.common'
    verbose_name = 'Common'

    def ready(self):
        if settings.DEV_SERVER and settings.USE_NGROK:
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
            settings.PROJECT_HOST = public_url
            CommonConfig.init_webhooks(public_url)

    @staticmethod
    def init_webhooks(public_url):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, region=settings.TWILIO_REGION)

        phone_number = client.incoming_phone_numbers.list(phone_number=settings.TWILIO_PHONE_NUMBER)[0]
        sms_callback_url = "{}/api/webhooks/sms".format(public_url)
        voice_callback_url = "{}/api/webhooks/voice".format(public_url)
        client.incoming_phone_numbers(phone_number.sid).update(voice_url=voice_callback_url,
                                                               sms_url=sms_callback_url)

        resource_name = 'twiltwil_' + os.environ.get('ENVIRONMENT')

        post_webhook_url = "{}/api/webhooks/chat/event".format(public_url)
        for service in client.chat.services.list():
            if service.friendly_name == resource_name:
                client.chat.services(service.sid).update(post_webhook_url=post_webhook_url)

        event_callback_url = "{}/api/webhooks/taskrouter/workspace".format(public_url)
        workspaces = client.taskrouter.workspaces.list(friendly_name=resource_name)
        if len(workspaces) > 0:
            client.taskrouter.workspaces(workspaces[0].sid).update(event_callback_url=event_callback_url)

            assignment_callback_url = "{}/api/webhooks/taskrouter/workflow".format(public_url)
            for workflow in client.taskrouter.workspaces(workspaces[0].sid).workflows.list():
                client.taskrouter.workspaces(workspaces[0].sid).workflows(workflow.sid).update(
                    assignment_callback_url=assignment_callback_url)
