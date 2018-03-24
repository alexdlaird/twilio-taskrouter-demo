"""
Authentication service functions.
"""

import logging

from django.contrib.auth import logout, get_user_model, login
from django.core.urlresolvers import reverse

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)


def process_register(request, user):
    """
    At this point the user will be created in the database and a worker created.

    :param request: the request
    :param user: the user that has been created
    :return: a redirect for the next page in the registration flow
    """
    logger.info('Registered new user with username: {}'.format(user.get_username()))

    user = get_user_model().objects.get(username=user.username)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    # TODO: create a TaskRouter worker, then update the User model

    return reverse('portal')


def process_logout(request):
    """
    Log the authenticated user out, then delete them.

    :param request: the request
    :return:
    """
    username = request.user.username
    logout(request)

    user = get_user_model().objects.get(username=username)
    if not user.is_superuser:
        user.delete()

    logger.info('Logged out and deleted user {}'.format(username))
