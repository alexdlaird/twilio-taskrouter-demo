"""
Manager for the User model.
"""

import logging

from django.contrib.auth.models import BaseUserManager
from django.db import models

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)


class UserQuerySet(models.query.QuerySet):
    def worker(self):
        return self.exclude(worked_sid__isnull=True)


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):  # pragma: no cover
        """
        Create a new user with the given username, password, and email.

        :param username: the username for the user
        :param password: the password for the new user
        :return: the created object
        """
        user = self.model(
            username=username
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):  # pragma: no cover
        """
        Create a new super user with admin privileges.

        :param username: the username for the user
        :param password: the password for the new user
        :return: the created object
        """
        user = self.create_user(username=username,
                                password=password)
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def worker(self):
        return self.get_queryset().worker()
