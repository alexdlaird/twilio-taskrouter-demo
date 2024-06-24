"""
Authentication view entrance functions.
"""

__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import logging

from django.http import HttpResponseRedirect
from django.urls import reverse

from twiltwil.auth.services import authservice

logger = logging.getLogger(__name__)


def logout(request):
    if request.user.is_authenticated:
        authservice.process_logout(request)

    return HttpResponseRedirect(reverse("home"))
