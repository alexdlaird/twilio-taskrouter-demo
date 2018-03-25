import json
import logging

from rest_framework.response import Response
from rest_framework.views import APIView

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)


class WebhookTaskRouterWorkspaceView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info('Workspace POST received: {}'.format(json.dumps(request.data)))

        return Response()
