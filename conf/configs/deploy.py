"""
Settings specific to prod-like deployable code, reading values from system environment variables.
"""

import os

from conf.settings import PROJECT_ID
from . import common

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.2'

# Application definition

INSTALLED_APPS = common.INSTALLED_APPS

MIDDLEWARE = common.MIDDLEWARE

TEMPLATES = common.TEMPLATES

if common.DEBUG:
    TEMPLATES[0]['OPTIONS']['context_processors'] += (
        'django.template.context_processors.debug',
    )

#############################
# Django configuration
#############################

# Security

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# Logging

if not common.DEBUG:
    ADMINS = (
        (common.PROJECT_NAME, common.ADMIN_EMAIL_ADDRESS),
    )
    MANAGERS = ADMINS

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
        'django_log': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/{}/django.log'.format(PROJECT_ID),
            'maxBytes': 50000000,
            'backupCount': 3,
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        '{}_common_log'.format(PROJECT_ID): {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/{}/common.log'.format(PROJECT_ID),
            'maxBytes': 50000000,
            'backupCount': 3,
            'formatter': 'standard',
        },
        '{}_auth_log'.format(PROJECT_ID): {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/{}/auth.log'.format(PROJECT_ID),
            'maxBytes': 50000000,
            'backupCount': 3,
            'formatter': 'standard',
        },
        '{}_portal_log'.format(PROJECT_ID): {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/{}/portal.log'.format(PROJECT_ID),
            'maxBytes': 50000000,
            'backupCount': 3,
            'formatter': 'standard',
        },
        '{}_api_log'.format(PROJECT_ID): {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/{}/api.log'.format(PROJECT_ID),
            'maxBytes': 50000000,
            'backupCount': 3,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['django_log', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'twiltwil.common': {
            'handlers': ['{}_common_log'.format(PROJECT_ID), 'mail_admins'],
            'level': 'INFO',
        },
        'twiltwil.auth': {
            'handlers': ['{}_auth_log'.format(PROJECT_ID), 'mail_admins'],
            'level': 'INFO',
        },
        'twiltwil.portal': {
            'handlers': ['{}_portal_log'.format(PROJECT_ID), 'mail_admins'],
            'level': 'INFO',
        },
        'twiltwil.api': {
            'handlers': ['{}_api_log'.format(PROJECT_ID), 'mail_admins'],
            'level': 'INFO',
        },
    }
}

# Cache

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('TWILTWIL_REDIS_HOST'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
}

# Database

DATABASES = {
    'default': {
        'NAME': os.environ.get('TWILTWIL_DB_NAME'),
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ.get('TWILTWIL_DB_HOST'),
        'USER': os.environ.get('TWILTWIL_DB_USER'),
        'PASSWORD': os.environ.get('TWILTWIL_DB_PASSWORD'),
    }
}
