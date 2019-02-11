"""
Context processors for project-specific attributes to be passed to all templates.
"""
import phonenumbers
from django.conf import settings

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.1.0"


def template(request):
    """
    Append project-specific attributes to a request context.

    :param request: the page request
    :return: a dictionary of context elements
    """
    context = {
        'PROJECT_NAME': settings.PROJECT_NAME,
        'PROJECT_VERSION': settings.PROJECT_VERSION,
        'PHONE_NUMBER': phonenumbers.format_number(phonenumbers.parse(settings.TWILIO_PHONE_NUMBER),
                                                   phonenumbers.PhoneNumberFormat.NATIONAL)
    }
    return context
