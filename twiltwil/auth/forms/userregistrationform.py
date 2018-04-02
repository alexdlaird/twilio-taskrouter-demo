import logging

from django import forms
from django.contrib.auth import get_user_model
from twilio.base.exceptions import TwilioRestException

from twiltwil.auth.models import Language, Skill
from twiltwil.auth.services import twilioauthservice
from twiltwil.common import enums
from twiltwil.common.forms.baseform import BaseForm

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)


class UserRegisterForm(forms.ModelForm, BaseForm):
    time_zone = forms.ChoiceField(label='Time zone', choices=enums.TIME_ZONE_CHOICES)

    languages = forms.ModelMultipleChoiceField(queryset=Language.objects.all())

    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all())

    class Meta:
        model = get_user_model()
        fields = ['username', 'time_zone', 'languages', 'skills', 'worker_sid']

    def clean(self):
        cleaned_data = super().clean()

        attributes = {
            "time_zone": cleaned_data['time_zone'],
            "languages": self.data['languages'],
            "skills": self.data['skills']
        }

        try:
            cleaned_data['worker_sid'] = twilioauthservice.create_worker(cleaned_data['username'], attributes).sid
        except TwilioRestException as e:
            if 'already exists' not in e.msg:
                logger.warning(e)

                raise forms.ValidationError("Oops, an unknown error occurred.")

            # If the Worker exists in Twilio but not in our database, it's orphaned, so just recreate it
            worker = twilioauthservice.get_worker_by_username(cleaned_data['username'])[0]
            twilioauthservice.delete_worker(worker.sid)
            cleaned_data['worker_sid'] = twilioauthservice.create_worker(cleaned_data['username'], attributes).sid

        return cleaned_data
