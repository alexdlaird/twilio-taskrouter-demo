"""
Context processors for project-specific attributes to be passed to all templates.
"""

from django.conf import settings

from twiltwil.auth.services import twilioauthservice

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

_TWILIO_SMS_FROM_FORMATTED = twilioauthservice.get_formatted_number(settings.TWILIO_SMS_FROM)


def template(request):
    """
    Append project-specific attributes to a request context.

    :param request: the page request
    :return: a dictionary of context elements
    """
    context = {
        'PROJECT_NAME': settings.PROJECT_NAME,
        'PROJECT_VERSION': settings.PROJECT_VERSION,
        'PHONE_NUMBER': _TWILIO_SMS_FROM_FORMATTED
    }
    return context
