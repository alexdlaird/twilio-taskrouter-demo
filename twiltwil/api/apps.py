__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'twiltwil.api'
    verbose_name = 'API'
    default_auto_field = 'django.db.models.AutoField'
