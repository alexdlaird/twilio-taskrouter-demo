"""
Settings specific to prod-like deployable code, reading values from system environment variables.
"""

import os

from .common import DEFAULT_TEMPLATES, DEFAULT_MIDDLEWARE, DEFAULT_INSTALLED_APPS, DEBUG, PROJECT_NAME, \
    ADMIN_EMAIL_ADDRESS

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

# Application definition

INSTALLED_APPS = DEFAULT_INSTALLED_APPS

MIDDLEWARE = DEFAULT_MIDDLEWARE

TEMPLATES = DEFAULT_TEMPLATES

if DEBUG:
    TEMPLATES[0]['OPTIONS']['context_processors'] += (
        'django.template.context_processors.debug',
    )

#############################
# Django configuration
#############################

# Security

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# Logging

if not DEBUG:
    ADMINS = (
        (PROJECT_NAME, ADMIN_EMAIL_ADDRESS),
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
            'filename': '/var/log/chachatwilio/django.log',
            'maxBytes': 50000000,
            'backupCount': 3,
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'chachatwilio_common_log': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/chachatwilio/chachatwilio_common.log',
            'maxBytes': 50000000,
            'backupCount': 3,
            'formatter': 'standard',
        },
        'chachatwilio_auth_log': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/chachatwilio/chachatwilio_auth.log',
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
        'chachatwilio.common': {
            'handlers': ['chachatwilio_common_log', 'mail_admins'],
            'level': 'INFO',
        },
        'chachatwilio.auth': {
            'handlers': ['chachatwilio_auth_log', 'mail_admins'],
            'level': 'INFO',
        },
    }
}

# Cache

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('CHACHATWILIO_REDIS_HOST'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
}

# Database

DATABASES = {
    'default': {
        'NAME': os.environ.get('CHACHATWILIO_DB_NAME'),
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ.get('CHACHATWILIO_DB_HOST'),
        'USER': os.environ.get('CHACHATWILIO_DB_USER'),
        'PASSWORD': os.environ.get('CHACHATWILIO_DB_PASSWORD'),
    }
}