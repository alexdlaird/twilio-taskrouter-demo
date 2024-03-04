__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

from django.urls import reverse

from twiltwil.auth.tests.helpers import userhelper
from twiltwil.common.tests.twiltwiltestcase import TwilTwilTestCase


class TestCaseCommonViews(TwilTwilTestCase):
    def test_home_view(self):
        # GIVEN
        userhelper.given_a_user_exists_and_is_logged_in(self.client)

        # WHEN
        response = self.client.get(reverse('home'))

        # THEN
        self.assertRedirects(response, reverse('portal'))
