__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

from django.contrib.auth import get_user_model

from twiltwil.auth.models import Language, Skill


def given_a_user_exists(username='test_user', password='test_pass_1!', time_zone='America/Los_Angeles', languages=None,
                        skills=None):
    if languages is None:
        languages = ['english']
    if skills is None:
        skills = ['general']

    user = get_user_model().objects.create_user(username=username,
                                                password=password)

    if user.time_zone != time_zone:
        user.time_zone = time_zone
        user.save()

    for language in languages:
        user.languages.add(Language.objects.get(id=language))
    for skill in skills:
        user.skills.add(Skill.objects.get(id=skill))

    return user


def given_a_user_exists_and_is_logged_in(client, username='test_user', password='test_pass_1!',
                                         time_zone='America/Los_Angeles', languages=None,
                                         skills=None, worker_sid='WORKERSID12345'):
    user = given_a_user_exists(username, password, time_zone, languages, skills)

    user.worker_sid = worker_sid
    user.save()

    client.login(username=user.get_username(), password=password)

    return user


def verify_user_not_logged_in(test_case):
    test_case.assertNotIn('_auth_user_id', test_case.client.session)


def verify_user_logged_in(test_case):
    test_case.assertIn('_auth_user_id', test_case.client.session)
