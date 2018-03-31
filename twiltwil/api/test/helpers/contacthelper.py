from twiltwil.api.models import Contact

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'


def given_a_contact_exists(sid='CONTACT12345', first_name='John', last_name='Doe', phone_number='+15555555555',
                           email='jon@example.com'):
    contact = Contact.objects.create(sid=sid,
                                     first_name=first_name,
                                     last_name=last_name,
                                     phone_number=phone_number,
                                     email=email)

    return contact
