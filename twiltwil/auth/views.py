"""
Authentication view entrance functions.
"""

import logging

from django.http import HttpResponseRedirect
from django.urls import reverse

from twiltwil.auth.services import authservice

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.1.0"

logger = logging.getLogger(__name__)


def logout(request):
    if request.user.is_authenticated():
        authservice.process_logout(request)

    return HttpResponseRedirect(reverse('home'))
