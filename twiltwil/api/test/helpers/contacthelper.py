__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

from twiltwil.api.models import Contact


def given_a_contact_exists(uuid="5082e5c3-28a8-4541-8e85-beedeba4ca43", first_name="John", last_name="Doe", phone_number="+15555555555",
                           email="jon@example.com"):
    contact = Contact.objects.create(uuid=uuid,
                                     first_name=first_name,
                                     last_name=last_name,
                                     phone_number=phone_number,
                                     email=email)

    return contact
