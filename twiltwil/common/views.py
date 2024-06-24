__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

"""
Unauthenticated general view entrance functions.
"""

import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from twiltwil.auth.forms.userregistrationform import UserRegisterForm
from twiltwil.auth.services import authservice
from twiltwil.common.utils.viewutils import set_request_status, get_request_status

logger = logging.getLogger(__name__)


def home(request):
    redirect = None

    if request.user.is_authenticated:
        redirect = reverse("portal")

    if request.method == "POST":
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            user_register_form.save()

            redirect = authservice.process_register(request, user_register_form.instance)
        else:
            set_request_status(request, "warning", list(user_register_form.errors.values())[0][0])
    else:
        user_register_form = UserRegisterForm()

    # Check if a status has been set (either by this view or another view from which we were redirect)
    status = get_request_status(request, "")

    if redirect:
        response = HttpResponseRedirect(redirect)

        return response
    else:
        data = {
            "form": user_register_form,
            "status": status
        }

        return render(request, "home.html", data)
