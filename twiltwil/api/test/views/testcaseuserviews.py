__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

from django.urls import reverse
from rest_framework import status

from twiltwil.auth.tests.helpers import userhelper
from twiltwil.common.tests.twiltwiltestcase import TwilTwilTestCase


class TestCaseUserViews(TwilTwilTestCase):
    def test_user_get(self):
        # GIVEN
        user = userhelper.given_a_user_exists_and_is_logged_in(self.client)

        # WHEN
        response = self.client.get(reverse('api_user'))

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {
                             "id": user.pk,
                             "username": "test_user",
                             "worker_sid": "WORKERSID12345",
                             "time_zone": "America/Los_Angeles",
                             "languages": ["english"],
                             "skills": ["general"]
                         })
