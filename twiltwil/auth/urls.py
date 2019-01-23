"""
Authentication URLs.
"""

from django.conf.urls import url

from twiltwil.auth.views import logout

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.1.0"

urlpatterns = [
    # Authentication URLs
    url(r'^logout', logout, name='logout'),
]
