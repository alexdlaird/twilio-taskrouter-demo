"""
API URLs.
"""
from django.conf.urls import url

from twiltwil.api.views.chattokenview import ChatTokenView
from twiltwil.api.views.userview import UserView
from twiltwil.api.views.webhookchateventview import WebhookChatEventView
from twiltwil.api.views.webhookmessengerview import WebhookMessengerView
from twiltwil.api.views.webhooksmsview import WebhookSmsView
from twiltwil.api.views.webhooktaskrouterworkflowview import WebhookTaskRouterWorkflowView
from twiltwil.api.views.webhooktaskrouterworkspaceview import WebhookTaskRouterWorkspaceView
from twiltwil.api.views.webhookvoiceview import WebhookVoiceView
from twiltwil.api.views.workertokenview import WorkerTokenView

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

urlpatterns = [
    # TwilTwil REST URLs
    url(r'^api/user$', UserView.as_view(), name='api_user'),

    # Twilio REST URLs
    url(r'^api/chat/token$', ChatTokenView.as_view(), name='api_chat_token'),
    url(r'^api/workers/token$', WorkerTokenView.as_view(), name='api_workers_token'),
    url(r'^api/webhooks/voice$', WebhookVoiceView.as_view(), name='api_webhooks_voice'),
    url(r'^api/webhooks/sms$', WebhookSmsView.as_view(), name='api_webhooks_sms'),
    url(r'^api/webhooks/chat/event$', WebhookChatEventView.as_view(), name='api_webhooks_chat_event'),
    url(r'^api/webhooks/taskrouter/workspace$', WebhookTaskRouterWorkspaceView.as_view(),
        name='api_webhooks_taskrouter_workspace'),
    url(r'^api/webhooks/taskrouter/workflow$', WebhookTaskRouterWorkflowView.as_view(),
        name='api_webhooks_taskrouter_workflow'),

    # Messenger Webhook URLs
    url(r'^api/webhooks/messenger$', WebhookMessengerView.as_view(), name='api_webhooks_messenger'),
]
