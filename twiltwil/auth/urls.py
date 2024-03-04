"""
Authentication URLs.
"""

__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

from django.urls import re_path

from twiltwil.auth.views import logout

urlpatterns = [
    # Authentication URLs
    re_path(r'^logout', logout, name='logout'),
]
