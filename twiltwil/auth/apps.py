from django.apps import AppConfig
from django.db import connection

from twiltwil.common import enums

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'


class AuthConfig(AppConfig):
    name = 'twiltwil.auth'
    label = 'twiltwil_auth'
    verbose_name = 'Authentication'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import twiltwil.auth.handlers

        AuthConfig.init_languages_and_skills()

    @staticmethod
    def init_languages_and_skills():
        from twiltwil.auth.models import Language, Skill

        if Language._meta.db_table not in connection.introspection.table_names() or Skill._meta.db_table not in connection.introspection.table_names():
            return

        for language in enums.LANGUAGE_CHOICES:
            Language.objects.get_or_create(id=language[0], defaults={
                'id': language[0],
                'name': language[1],
            })

        for skill in enums.SKILL_CHOICES:
            Skill.objects.get_or_create(id=skill[0], defaults={
                'id': skill[0],
                'name': skill[1],
            })
