"""
User model.
"""

__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import logging

from django.contrib.auth.models import AbstractBaseUser
from django.core import validators
from django.db import models

from twiltwil.common import enums
from twiltwil.common.models.base import BaseModel
from ..managers.usermanager import UserManager

logger = logging.getLogger(__name__)


class User(AbstractBaseUser, BaseModel):
    # Authentication fields

    username = models.CharField(help_text='A unique name used to login to the system.',
                                max_length=255, unique=True,
                                validators=[validators.RegexValidator(r'^[\w.@+-]+$',
                                                                      'Enter a valid username, which means less than '
                                                                      '30 characters consisting of letters, numbers, '
                                                                      'or these symbols: @+-_.',
                                                                      'invalid'), ],
                                error_messages={'unique': "Sorry, that username is already in use."})

    is_superuser = models.BooleanField(default=False)

    # Profile fields

    time_zone = models.CharField(default='America/Los_Angeles', max_length=255, choices=enums.TIME_ZONE_CHOICES)

    languages = models.ManyToManyField('Language', blank=True, default=None)

    skills = models.ManyToManyField('Skill', blank=True, default=None)

    worker_sid = models.CharField(max_length=255, blank=True, null=True, unique=True)

    # Set the manager
    objects = UserManager()

    # Fields required to define the abstracted Django user
    USERNAME_FIELD = 'username'

    def get_full_name(self):  # pragma: no cover
        """
        Retrieve the long name for the user.

        :return: The user's username.
        """
        return self.username

    def get_short_name(self):  # pragma: no cover
        """
        Retrieve the short name for the user.

        :return: The user's username.
        """
        return self.username

    def has_perm(self, perm, obj=None):  # pragma: no cover
        """
        Check if this user has the given permission.

        :param perm: The permission to check for.
        :param obj: The object to check for permissions
        :return: True if the user has the permission, False otherwise.
        """
        return True

    def has_module_perms(self, app_label):  # pragma: no cover
        """
        Check if the user has privileges to the given app.

        :param app_label: The label of the app on which to check for permissions.
        :return: True if the user has privileges for app, False otherwise
        """
        return True

    @property
    def is_staff(self):  # pragma: no cover
        """
        Check if this user has administrative privileges.

        :return: True if the user is an admin, False otherwise
        """
        return self.is_superuser
