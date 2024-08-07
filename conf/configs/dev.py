"""
Settings specific to a development environment using Django's `runserver` command, reading values from `.env`.
"""

__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import os
import warnings

from conf.settings import PROJECT_ID
from . import common

# Define the base working directory of the application
BASE_DIR = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..'))

# Application definition

INSTALLED_APPS = common.INSTALLED_APPS + (
    'debug_toolbar',
)

MIDDLEWARE = common.MIDDLEWARE + (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATES = common.TEMPLATES

TEMPLATES[0]['OPTIONS']['context_processors'] += (
    'django.template.context_processors.debug',
)

#############################
# Django configuration
#############################

# Security

INTERNAL_IPS = (
    '127.0.0.1',
)

ALLOWED_HOSTS = common.ALLOWED_HOSTS + [
    '.ngrok.io',
    '.ngrok.app'
]

CSRF_TRUSTED_ORIGINS = common.CSRF_TRUSTED_ORIGINS + [
    'https://*.ngrok.io',
    'https://*.ngrok.app'
]

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        str(PROJECT_ID): {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}

# When in development, we want to be warned about dates that don't have a timezone
warnings.filterwarnings('error', r"DateTimeField .* received a naive datetime", RuntimeWarning,
                        r'django\.db\.models\.fields')

# Cache

if os.environ.get('USE_IN_MEMORY_DB', 'True') == 'True':
    CACHES = {
        'default': {
            'BACKEND': 'twiltwil.common.cache.locmemkeys.LocMemKeysCache',
            'LOCATION': 'unique-snowflake',
        }
    }
else:
    from conf.configs import deploy, common

    SESSION_ENGINE = deploy.SESSION_ENGINE
    CACHES = deploy.CACHES

# Database

if os.environ.get('USE_IN_MEMORY_DB', 'True') == 'True':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    from conf.configs import deploy

    DATABASES = deploy.DATABASES

# Pipelines

common.PIPELINE['CSS_COMPRESSOR'] = None
common.PIPELINE['JS_COMPRESSOR'] = None
