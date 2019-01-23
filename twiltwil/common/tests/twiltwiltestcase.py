from django.test import TestCase

from twiltwil.auth.apps import AuthConfig

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.1.0"


class TwilTwilTestCase(TestCase):
    def setUp(self):
        AuthConfig.init_languages_and_skills()
