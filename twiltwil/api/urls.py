"""
API URLs.
"""
from django.conf.urls import url

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
__version__ = "0.2.0"

urlpatterns = [
    # TwilTwil REST URLs
    url(r'^api/user$', UserView.as_view(), name='api_user'),
    url(r'^api/contacts/(?P<uuid>[-\w]+)$', ContactView.as_view(), name='api_contacts_detail'),
    url(r'^api/info$', InfoView.as_view(), name='api_info'),

    # Webhook REST URLs
    url(r'^api/chat/token$', ChatTokenView.as_view(), name='api_chat_token'),
    url(r'^api/voice/token$', VoiceTokenView.as_view(), name='api_voice_token'),
    url(r'^api/workspace/token$', WorkspaceTokenView.as_view(), name='api_workspace_token'),
    url(r'^api/workers/token$', WorkerTokenView.as_view(), name='api_workers_token'),
    url(r'^api/webhooks/voice$', WebhookVoiceView.as_view(), name='api_webhooks_voice'),
    url(r'^api/webhooks/voice/enqueue$', WebhookVoiceEnqueueView.as_view(), name='api_webhooks_voice_enqueue'),
    url(r'^api/webhooks/voice/conference$', WebhookVoiceConferenceView.as_view(), name='api_webhooks_voice_conference'),
    url(r'^api/webhooks/sms$', WebhookSmsView.as_view(), name='api_webhooks_sms'),
    url(r'^api/webhooks/chat/event$', WebhookChatEventView.as_view(), name='api_webhooks_chat_event'),
    url(r'^api/webhooks/taskrouter/workspace$', WebhookTaskRouterWorkspaceView.as_view(),
        name='api_webhooks_taskrouter_workspace'),
    url(r'^api/webhooks/taskrouter/workflow$', WebhookTaskRouterWorkflowView.as_view(),
        name='api_webhooks_taskrouter_workflow'),
]
