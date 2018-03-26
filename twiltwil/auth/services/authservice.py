"""
Authentication service functions.
"""

import logging

from django.contrib.auth import logout, get_user_model, login
from django.core.urlresolvers import reverse

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

    attributes = {
        "time_zone": user.time_zone,
        "languages": list(user.languages.all().values_list('id', flat=True)),
        "skills": list(user.skills.all().values_list('id', flat=True))
    }

    worker = twilioauthservice.create_worker(user.username, attributes)

    user.worker_sid = worker.sid
    user.save()

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
        user.delete()

    logger.info('Logged out and deleted user {}'.format(username))
