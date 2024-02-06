"""
Authenticated app URLs.
"""

from django.urls import re_path

from twiltwil.portal.views import portal

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.3.0"

urlpatterns = [
    # Authenticated URLs
    re_path(r'^portal', portal, name='portal'),
]
