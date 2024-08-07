__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import json
import logging

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from twiltwil.api.models import Message
from twiltwil.api.services import twilioservice
from twiltwil.api.utils import messageutils
from twiltwil.auth.services import authservice

logger = logging.getLogger(__name__)


class WebhookTaskRouterWorkspaceView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info(f"Workspace POST received: {json.dumps(request.data)}")

        if "EventType" in request.data:
            if request.data["EventType"] == "reservation.created":
                task_attributes = json.loads(messageutils.cleanup_json(request.data["TaskAttributes"]))

                conversation = twilioservice.get_conversation(task_attributes["conversation"])

                twilioservice.add_worker_to_conversation(conversation, request.data["WorkerName"])
            elif request.data["EventType"] == "reservation.accepted":
                logger.info("Processing reservation.accepted")

                task_attributes = json.loads(messageutils.cleanup_json(request.data["TaskAttributes"]))

                if "from" in task_attributes:
                    for message in Message.objects.not_resolved().for_channel("sms").inbound().for_contact(
                            task_attributes["from"]).no_worker().iterator():
                        message.worker_sid = request.data["WorkerSid"]

                        message.save()
            elif request.data["EventType"] == "task.created":
                logger.info("Processing task.created")

                task_attributes = json.loads(messageutils.cleanup_json(request.data["TaskAttributes"]))

                if "from" in task_attributes:
                    for message in Message.objects.not_resolved().for_channel("sms").inbound().for_contact(
                            task_attributes["from"]).no_worker().iterator():
                        message.task_sid = request.data["TaskSid"]

                        message.save()
            elif request.data["EventType"] == "task.canceled":
                logger.info("Processing task.canceled")

                task_attributes = json.loads(messageutils.cleanup_json(request.data["TaskAttributes"]))

                conversation = twilioservice.get_conversation(task_attributes["conversation"])

                cancelled_message = "Sorry, your question could not be answered because the agent assigned to it is " \
                                    "no longer available. Try submitting it again!"
                twilioservice.send_conversation_message(conversation,
                                                        None,
                                                        cancelled_message)
            elif request.data["EventType"] == "task.completed":
                logger.info("Processing task.completed")

                # TODO: once TaskRouter supports Task transfer, we could utilize that here instead
                if "TaskCompletedReason" in request.data and request.data["TaskCompletedReason"].startswith(
                        "User logged out"):
                    task_attributes = json.loads(messageutils.cleanup_json(request.data["TaskAttributes"]))

                    twilioservice.create_task(task_attributes)

                for message in Message.objects.for_task(request.data["TaskSid"]).iterator():
                    message.worker_sid = None
                    message.resolved = True
                    message.save()
            elif request.data["EventType"] == "worker.deleted":
                try:
                    user = get_user_model().objects.get(worker_sid=request.data["WorkerSid"])
                    authservice.delete_user(user)
                except get_user_model().DoesNotExist:
                    pass

        return Response(status=status.HTTP_204_NO_CONTENT)
