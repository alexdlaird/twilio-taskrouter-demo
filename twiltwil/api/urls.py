"""
API URLs.
"""
from django.urls import re_path

from twiltwil.api.views.chattokenview import ChatTokenView
from twiltwil.api.views.contactview import ContactView
from twiltwil.api.views.infoview import InfoView
from twiltwil.api.views.userview import UserView
from twiltwil.api.views.voicetokenview import VoiceTokenView
from twiltwil.api.views.webhookchateventview import WebhookChatEventView
from twiltwil.api.views.webhooksmsview import WebhookSmsView
from twiltwil.api.views.webhooktaskrouterworkflowview import WebhookTaskRouterWorkflowView
from twiltwil.api.views.webhooktaskrouterworkspaceview import WebhookTaskRouterWorkspaceView
from twiltwil.api.views.webhookvoiceconferenceview import WebhookVoiceConferenceView
from twiltwil.api.views.webhookvoiceenqueueview import WebhookVoiceEnqueueView
from twiltwil.api.views.webhookvoiceview import WebhookVoiceView
from twiltwil.api.views.workertokenview import WorkerTokenView
from twiltwil.api.views.workspacetokenview import WorkspaceTokenView

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.3.0"

urlpatterns = [
    # TwilTwil REST URLs
    re_path(r'^api/user$', UserView.as_view(), name='api_user'),
    re_path(r'^api/contacts/(?P<uuid>[-\w]+)$', ContactView.as_view(), name='api_contacts_detail'),
    re_path(r'^api/info$', InfoView.as_view(), name='api_info'),

    # Webhook REST URLs
    re_path(r'^api/chat/token$', ChatTokenView.as_view(), name='api_chat_token'),
    re_path(r'^api/voice/token$', VoiceTokenView.as_view(), name='api_voice_token'),
    re_path(r'^api/workspace/token$', WorkspaceTokenView.as_view(), name='api_workspace_token'),
    re_path(r'^api/workers/token$', WorkerTokenView.as_view(), name='api_workers_token'),
    re_path(r'^api/webhooks/voice$', WebhookVoiceView.as_view(), name='api_webhooks_voice'),
    re_path(r'^api/webhooks/voice/enqueue$', WebhookVoiceEnqueueView.as_view(), name='api_webhooks_voice_enqueue'),
    re_path(r'^api/webhooks/voice/conference$', WebhookVoiceConferenceView.as_view(),
            name='api_webhooks_voice_conference'),
    re_path(r'^api/webhooks/sms$', WebhookSmsView.as_view(), name='api_webhooks_sms'),
    re_path(r'^api/webhooks/chat/event$', WebhookChatEventView.as_view(), name='api_webhooks_chat_event'),
    re_path(r'^api/webhooks/taskrouter/workspace$', WebhookTaskRouterWorkspaceView.as_view(),
            name='api_webhooks_taskrouter_workspace'),
    re_path(r'^api/webhooks/taskrouter/workflow$', WebhookTaskRouterWorkflowView.as_view(),
            name='api_webhooks_taskrouter_workflow'),
]
