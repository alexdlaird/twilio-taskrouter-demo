"""
Settings common to all deployment methods.
"""

import os
import socket

from conf.settings import PROJECT_ID

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.2'

# Define the base working directory of the application
BASE_DIR = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..'))

# ############################
# Project configuration
# ############################

# Project information

PROJECT_NAME = os.environ.get('TWILTWIL_NAME')

PROJECT_HOST = os.environ.get('TWILTWIL_HOST')

# Version information

PROJECT_VERSION = __version__

#############################
# Default lists for host-specific configurations
#############################

INSTALLED_APPS = (
    # Django modules
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    # Third-party modules
    'pipeline',
    'widget_tweaks',
    'rest_framework',
    # Project modules
    'twiltwil.common',
    'twiltwil.auth',
    'twiltwil.portal',
    'twiltwil.api',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
            'django.template.context_processors.request',
            'twiltwil.common.handlers.processors.template',
        ],
        'debug': os.environ.get('TWILTWIL_TEMPLATE_DEBUG', 'False') == 'True'
    },
}]

#############################
# Django configuration
#############################

# Application definition

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
AUTH_USER_MODEL = 'twiltwil_auth.User'
LOGIN_URL = '/'
LOGOUT_URL = '/logout'
ROOT_URLCONF = 'conf.urls'
WSGI_APPLICATION = 'conf.wsgi.application'

HOSTNAME = socket.gethostname()

# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_THOUSAND_SEPARATOR = True
USE_TZ = True
HE_DATE_STRING = "%Y-%m-%d"
HE_TIME_STRING = "%H:%M:%S"
HE_DATE_TIME_STRING = HE_DATE_STRING + " " + HE_TIME_STRING

# Email settings

ADMIN_EMAIL_ADDRESS = os.environ.get('TWILTWIL_ADMIN_EMAIL')
SERVER_EMAIL = ADMIN_EMAIL_ADDRESS
EMAIL_USE_TLS = os.environ.get('TWILTWIL_EMAIL_USE_TLS', 'True') == 'True'
EMAIL_PORT = os.environ.get('TWILTWIL_EMAIL_PORT')
EMAIL_ADDRESS = os.environ.get('TWILTWIL_CONTACT_EMAIL')
DEFAULT_FROM_EMAIL = '{} <{}>'.format(PROJECT_NAME, EMAIL_ADDRESS)
EMAIL_HOST = os.environ.get('TWILTWIL_EMAIL_HOST')

EMAIL_HOST_USER = os.environ.get('TWILTWIL_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('TWILTWIL_EMAIL_HOST_PASSWORD')

# Authentication

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Security

SECRET_KEY = os.environ.get('TWILTWIL_SECRET_KEY')
CSRF_COOKIE_SECURE = os.environ.get('TWILTWIL_CSRF_COOKIE_SECURE', 'True') == 'True'
SESSION_COOKIE_SECURE = os.environ.get('TWILTWIL_SESSION_COOKIE_SECURE', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('TWILTWIL_ALLOWED_HOSTS').split(' ')
CSRF_MIDDLEWARE_SECRET = os.environ.get('TWILTWIL_CSRF_MIDDLEWARE_SECRET')

# Logging

DEBUG = os.environ.get('TWILTWIL_DEBUG', 'False') == 'True'

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

# Media files

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Pipelines

PIPELINE = {
    'DISABLE_WRAPPER': True,
    'STYLESHEETS': {
        'base': {
            'source_filenames': (
                'css/base.css',
            ),
            'output_filename': 'css/{}_base_{}.min.css'.format(PROJECT_ID, PROJECT_VERSION)
        },
        'portal': {
            'source_filenames': (
                'css/portal.css',
            ),
            'output_filename': 'css/{}_portal_{}.min.css'.format(PROJECT_ID, PROJECT_VERSION)
        },
    },
    'JAVASCRIPT': {
        'portal': {
            'source_filenames': (
                'js/api.js',
                'js/portal.js',
                'js/taskrouter.1.20.min.js',
            ),
            'output_filename': 'js/{}_portal_{}.min.js'.format(PROJECT_ID, PROJECT_VERSION)
        },
    }
}

# Twilio

TWILIO_ACCOUNT_SID = os.environ.get('TWILTWIL_TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILTWIL_TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILTWIL_TWILIO_PHONE_NUMBER')
TWILIO_API_KEY = os.environ.get('TWILTWIL_TWILIO_API_KEY')
TWILIO_API_SECRET = os.environ.get('TWILTWIL_TWILIO_API_SECRET')

TWILIO_API_BASE_URL = os.environ.get('TWILTWIL_TWILIO_API_BASE_URL', None)
TWILIO_EVENT_BRIDGE_BASE_URL = os.environ.get('TWILTWIL_TWILIO_EVENT_BRIDGE_BASE_URL', None)
TWILIO_REGION = os.environ.get('TWILTWIL_TWILIO_REGION', None)

# Other

DISABLE_LOBBY_VIDEO = os.environ.get('TWILTWIL_DISABLE_LOBBY_VIDEO', 'False') == 'True'
MAX_HTTP_RETRIES = os.environ.get('TWILTWIL_MAX_HTTP_RETRIES', 5)
