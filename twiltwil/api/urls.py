"""
REST URLs.
"""
from django.conf.urls import url

from twiltwil.api.views.webhooksmsview import WebhookSmsView
from twiltwil.api.views.webhooktaskrouterworkflowview import WebhookTaskRouterWorkflowView
from twiltwil.api.views.webhooktaskrouterworkspaceview import WebhookTaskRouterWorkspaceView
from twiltwil.api.views.webhookvoiceview import WebhookVoiceView
from twiltwil.api.views.workertokenview import WorkerTokenView

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

urlpatterns = [
    # REST URLs
    url(r'^api/worker/token/$', WorkerTokenView.as_view(), name='api_worker_token'),
    url(r'^api/webhook/voice/$', WebhookVoiceView.as_view(), name='api_webhook_voice'),
    url(r'^api/webhook/sms/$', WebhookSmsView.as_view(), name='api_webhook_sms'),
    url(r'^api/webhook/taskrouter/workspace/$', WebhookTaskRouterWorkspaceView.as_view(),
        name='api_webhook_taskrouter_workspace'),
    url(r'^api/webhook/taskrouter/workflow/$', WebhookTaskRouterWorkflowView.as_view(),
        name='api_webhook_taskrouter_workflow'),
]
