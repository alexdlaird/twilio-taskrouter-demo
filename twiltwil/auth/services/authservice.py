"""
Authentication service functions.
"""

import logging

from django.contrib.auth import logout, get_user_model, login
from django.core.urlresolvers import reverse
from twilio.base.exceptions import TwilioRestException

from twiltwil.api.models import Message
from twiltwil.api.services import twilioservice
from twiltwil.auth.services import twilioauthservice

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)


def process_register(request, user):
    """
    At this point the user will be created in the database and a Twilio Worker instantiated.

    :param request: the request
    :param user: the user that has been created
    :return: a redirect to the next page in the registration flow
    """
    logger.info('Registered new user with username: {}'.format(user.get_username()))

    user = get_user_model().objects.get(username=user.username)

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    return reverse('portal')


def process_logout(request):
    """
    Logout the currently authenticated user, then delete the associated database entry and its Twilio Worker.

    :param request: the request
    :return:
    """
    username = request.user.username
    logout(request)

    user = get_user_model().objects.get(username=username)
    if not user.is_superuser:
        delete_user(user)

    logger.info('Logged out and deleted user {}'.format(username))


def delete_user(user):
    """
    Delete the given user from the database as well as Twilio's TaskRouter.

    :param user: the user to be deleted
    """
    username = user.username
    worker_sid = user.worker_sid

    user.delete()

    try:
        twilioservice.cancel_worker_tasks(username,
                                          Message.objects.not_resolved().inbound().for_worker(worker_sid).values_list(
                                              'task_sid',
                                              flat=True).distinct())

        for message in Message.objects.for_worker(worker_sid).iterator():
            message.worker_sid = None
            message.save()

        twilioauthservice.delete_worker(worker_sid)

        twilioauthservice.delete_chat_user(username)
    except TwilioRestException as e:
        if e.status != 404:
            raise e
