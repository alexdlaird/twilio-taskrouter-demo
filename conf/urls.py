"""
Base URL configuration.
"""

import sys

from django.conf import settings as config
from django.urls import include, re_path
from django.views import static

import twiltwil.auth.urls
import twiltwil.common.urls
import twiltwil.portal.urls
import twiltwil.api.urls

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.3.0'

urlpatterns = [
    # Include app-specific URL files
    re_path(r'^', include(twiltwil.common.urls)),
    re_path(r'^', include(twiltwil.auth.urls)),
    re_path(r'^', include(twiltwil.portal.urls)),
    re_path(r'^', include(twiltwil.api.urls)),
]

if config.DEBUG:
    import debug_toolbar

    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]

if config.DEBUG or 'test' in sys.argv:
    # Ensure media files are shown properly when using a dev server
    urlpatterns += [
        re_path(r'^' + config.MEDIA_URL.lstrip('/') + '(?P<path>.*)$', static.serve, {
            'document_root': config.MEDIA_ROOT})
    ]
