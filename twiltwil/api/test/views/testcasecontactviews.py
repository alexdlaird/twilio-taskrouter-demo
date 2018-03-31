from django.urls import reverse
from rest_framework import status

from twiltwil.api.test.helpers import contacthelper
from twiltwil.auth.tests.helpers import userhelper
from twiltwil.common.tests.twiltwiltestcase import TwilTwilTestCase

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'


class TestCaseContactViews(TwilTwilTestCase):
    def test_contact_get(self):
        # GIVEN
        userhelper.given_a_user_exists_and_is_logged_in(self.client)
        contact = contacthelper.given_a_contact_exists()

        # WHEN
        response = self.client.get(reverse('api_contacts_detail', args=(contact.sid,)))

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {
                             "id": contact.pk,
                             "sid": "CONTACT12345",
                             "first_name": "John",
                             "last_name": "Doe",
                             "phone_number": "+15555555555",
                             "email": "jon@example.com",
                             "card": "John Doe (P: (555) 555-5555, E: jon@example.com)"
                         })
