import json
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.1.0"

logger = logging.getLogger(__name__)


class WebhookTaskRouterWorkflowView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info(f'Workflow POST received: {json.dumps(request.data)}')

        return Response(status=status.HTTP_204_NO_CONTENT)
