__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import os
import sys
from urllib.parse import urlparse

from django.apps import AppConfig
from django.conf import settings


class ApiConfig(AppConfig):
    name = "twiltwil.api"
    verbose_name = "API"
    default_auto_field = "django.db.models.AutoField"

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

        ApiConfig.provision_twilio_resources()

    @staticmethod
    def provision_twilio_resources():
        from twiltwil.auth.services import twilioauthservice

        # Ensure Twilio resources are provisioned
        twilioauthservice.update_phone_number_webhooks()
        service = twilioauthservice.get_service()
        twilioauthservice.update_service_webhooks(service)
        workspace = twilioauthservice.get_workspace()
        twilioauthservice.update_workspace_webhooks(workspace)
        workflow = twilioauthservice.get_workflow()
        twilioauthservice.update_workflow_webhooks(workspace, workflow)
