import os
import sys
from urllib.parse import urlparse

from django.apps import AppConfig
from django.conf import settings
from pyngrok import ngrok
from twilio.rest import Client

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.1.2"


class CommonConfig(AppConfig):
    name = 'twiltwil.common'
    verbose_name = 'Common'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) and \
                settings.DEV_SERVER and settings.USE_NGROK:
            CommonConfig.init_ngrok()

    @staticmethod
    def init_ngrok():
        addrport = urlparse('http://{}'.format(sys.argv[-1]))
        port = addrport.port if addrport.netloc and addrport.port else 8000
        public_url = ngrok.connect(port)
        print('ngrok tunneling from {} -> http://127.0.0.1:{}/'.format(public_url, port))

        CommonConfig.init_webhook(public_url)

    @staticmethod
    def init_webhooks(callback_url):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        phone_number_sid = client.incoming_phone_numbers.list(phone_number=settings.TWILIO_SMS_FROM)[0].sid
        client.incoming_phone_numbers(phone_number_sid).update(sms_url=callback_url)
