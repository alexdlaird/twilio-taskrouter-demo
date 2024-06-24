__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import logging

from django import forms
from django.contrib.auth import get_user_model
from twilio.base.exceptions import TwilioRestException

from twiltwil.auth.models import Language, Skill
from twiltwil.auth.services import twilioauthservice
from twiltwil.common import enums
from twiltwil.common.forms.baseform import BaseForm

logger = logging.getLogger(__name__)


class UserRegisterForm(forms.ModelForm, BaseForm):
    time_zone = forms.ChoiceField(label="Time zone", choices=enums.TIME_ZONE_CHOICES)

    languages = forms.ModelMultipleChoiceField(queryset=Language.objects.all())

    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all())

    class Meta:
        model = get_user_model()
        fields = ["username", "time_zone", "languages", "skills", "worker_sid"]

    def clean(self):
        cleaned_data = super().clean()

        attributes = {
            "time_zone": cleaned_data["time_zone"],
            "languages": self.data.getlist("languages"),
            "skills": self.data.getlist("skills")
        }

        try:
            cleaned_data["worker_sid"] = twilioauthservice.create_worker(cleaned_data["username"], attributes).sid
        except TwilioRestException as e:
            # If the Worker exists in Twilio but not in our database, it"s orphaned, so just recreate it
            worker = twilioauthservice.get_worker_by_username(cleaned_data["username"])[0]
            twilioauthservice.delete_worker(worker.sid)
            cleaned_data["worker_sid"] = twilioauthservice.create_worker(cleaned_data["username"], attributes).sid

        return cleaned_data
