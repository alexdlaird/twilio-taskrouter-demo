import logging
from urllib.parse import unquote

from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.1.0"

logger = logging.getLogger(__name__)


def set_request_status(request, status_type, message):
    """
    Set a 'status' of {'type', 'msg'} on the given request.

    :param request: the request being processed.
    :param status_type: the type of status to be displayed (match to Bootstrap alert types)
    :param message: the status message to be display
    """
    request.session['status'] = {'type': status_type, 'msg': message}


def get_request_status(request, default=None):
    """
    Return the 'status' attribute on the current request, if it exists. If successful, remove it from the request so the
    status is not processed again.

    :param request: the request being processed
    :param default: the default status, if one is not found on the request
    :return:
    """
    status = request.session.get('status', default)

    if not status:
        status_type = request.COOKIES.get('status_type', None)
        status_msg = request.COOKIES.get('status_msg', None)
        if status_type and status_msg:
            status = {'type': status_type, 'msg': unquote(status_msg)}

    if 'status' in request.session:
        del request.session['status']

    return status


def get_empty_webhook_response():
    return HttpResponse(str(MessagingResponse()), content_type='text/xml')
