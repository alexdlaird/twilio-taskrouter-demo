from django import forms
from django.contrib.auth import get_user_model

from twiltwil.auth.models import Language, Skill
from twiltwil.auth.services import twilioauthservice
from twiltwil.common import enums
from twiltwil.common.forms.baseform import BaseForm

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'


class UserRegisterForm(forms.ModelForm, BaseForm):
    time_zone = forms.ChoiceField(label='Time zone', choices=enums.TIME_ZONE_CHOICES)

    languages = forms.ModelMultipleChoiceField(queryset=Language.objects.all())

    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all())

    class Meta:
        model = get_user_model()
        fields = ['username', 'time_zone', 'languages', 'skills']

    def save(self, commit=True):
        instance = super().save(False)

        attributes = {
            "time_zone": instance.time_zone,
            "languages": self.data.getlist('languages'),
            "skills": self.data.getlist('skills')
        }

        worker = twilioauthservice.create_worker(instance.username, attributes)

        instance.worker_sid = worker.sid

        if commit:
            instance.save()
            self.save_m2m()

        return instance
