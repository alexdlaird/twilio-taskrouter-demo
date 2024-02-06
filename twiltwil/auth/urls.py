"""
Authentication URLs.
"""

from django.urls import re_path

from twiltwil.auth.views import logout

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.3.0"

urlpatterns = [
    # Authentication URLs
    re_path(r'^logout', logout, name='logout'),
]
