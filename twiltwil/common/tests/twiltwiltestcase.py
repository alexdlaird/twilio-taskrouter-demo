__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

from django.test import TestCase

from twiltwil.auth.apps import AuthConfig


class TwilTwilTestCase(TestCase):
    def setUp(self):
        AuthConfig.init_languages_and_skills()
