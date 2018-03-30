import mock
from django.contrib.auth import get_user_model
from django.urls import reverse

from twiltwil.auth.tests.helpers import userhelper, twiliohelper
from twiltwil.common import enums
from twiltwil.common.tests.twiltwiltestcase import TwilTwilTestCase

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'


class TestCaseAuthViews(TwilTwilTestCase):
    @mock.patch('twiltwil.auth.services.authservice.twilioauthservice.create_worker')
    def test_registration_success(self, mock_create_worker):
        # GIVEN
        userhelper.verify_user_not_logged_in(self)
        mock_create_worker.return_value = twiliohelper.get_worker_instance()

        # WHEN
        response = self.client.post(reverse('home'),
                                    {'username': 'my_test_user', 'time_zone': 'America/Chicago',
                                     'languages': enums.SPANISH, 'skills': enums.ANIMALS})

        # THEN
        userhelper.verify_user_logged_in(self)
        user = get_user_model().objects.get(username='my_test_user')
        self.assertEqual(user.username, 'my_test_user')
        self.assertEqual(user.time_zone, 'America/Chicago')
        self.assertEqual(user.languages.all()[0].id, enums.SPANISH)
        self.assertEqual(user.skills.all()[0].id, enums.ANIMALS)
        self.assertRedirects(response, reverse('portal'))

    def test_registration_bad_data(self):
        # GIVEN
        userhelper.verify_user_not_logged_in(self)

        # WHEN
        response = self.client.post(reverse('home'),
                                    {'username': 'my_test_user', 'time_zone': 'America/Chicago', 'languages': 'invalid',
                                     'skills': enums.ANIMALS})

        # THEN
        userhelper.verify_user_not_logged_in(self)
        self.assertFalse(get_user_model().objects.filter(username='my_test_user').exists())
        self.assertContains(response, 'invalid is not one of the available choices')

    @mock.patch('twiltwil.auth.services.authservice.twilioauthservice.delete_worker')
    @mock.patch('twiltwil.auth.services.authservice.twilioauthservice.delete_chat_user')
    def test_logout_success(self, mock_delete_chat_user, mock_delete_worker):
        # GIVEN
        userhelper.given_a_user_exists_and_is_logged_in(self.client)

        # WHEN
        response = self.client.post(reverse('logout'))

        # THEN
        self.assertEqual(response.status_code, 302)
        userhelper.verify_user_not_logged_in(self)
        self.assertFalse(get_user_model().objects.filter(username='my_test_user').exists())

    def test_authenticated_view_success(self):
        # GIVEN
        user = userhelper.given_a_user_exists(self.client)

        # WHEN
        response1 = self.client.get(reverse('portal'))
        self.client.login(username=user.get_username(), password='test_pass_1!')
        response2 = self.client.get(reverse('portal'))

        # THEN
        self.assertRedirects(response1, reverse('home') + '?next={}'.format(reverse('portal')),
                             fetch_redirect_response=False)
        self.assertEqual(response2.status_code, 200)
