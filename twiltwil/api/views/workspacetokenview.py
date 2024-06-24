__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from twiltwil.auth.services import twilioauthservice

logger = logging.getLogger(__name__)


class WorkspaceTokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = {
            "token": twilioauthservice.get_workspace_token()
        }

        return Response(data)
