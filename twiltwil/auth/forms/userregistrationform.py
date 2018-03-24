from django import forms
from django.contrib.auth import get_user_model

from twiltwil.common import enums
from twiltwil.common.forms.baseform import BaseForm

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'


class UserRegisterForm(forms.ModelForm, BaseForm):
    time_zone = forms.ChoiceField(label='Time zone', choices=enums.TIME_ZONE_CHOICES)

    language = forms.ChoiceField(label='Language', choices=enums.LANGUAGE_CHOICES)

    class Meta:
        model = get_user_model()
        fields = ['username', 'time_zone', 'language']
