import logging

from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from twiltwil.auth.services import twilioauthservice

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.1.0"

logger = logging.getLogger(__name__)


class ChatTokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if 'username' not in request.data:
            raise serializers.ValidationError("'username' is required")

        data = {
            'token': twilioauthservice.get_chat_token(request.data['username'])
        }

        return Response(data)
