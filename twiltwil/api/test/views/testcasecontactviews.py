__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

from django.urls import reverse
from rest_framework import status

from twiltwil.api.test.helpers import contacthelper
from twiltwil.auth.tests.helpers import userhelper
from twiltwil.common.tests.twiltwiltestcase import TwilTwilTestCase


class TestCaseContactViews(TwilTwilTestCase):
    def test_contact_get(self):
        # GIVEN
        userhelper.given_a_user_exists_and_is_logged_in(self.client)
        contact = contacthelper.given_a_contact_exists()

        # WHEN
        response = self.client.get(reverse("api_contacts_detail", args=(contact.uuid,)))

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {
                             "id": contact.pk,
                             "uuid": "5082e5c3-28a8-4541-8e85-beedeba4ca43",
                             "first_name": "John",
                             "last_name": "Doe",
                             "phone_number": "+15555555555",
                             "email": "jon@example.com",
                             "card": "John Doe (P: (555) 555-5555, E: jon@example.com)"
                         })
