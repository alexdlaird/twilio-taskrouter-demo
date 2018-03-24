from django import forms

from chachatwilio.common.forms.baseform import BaseForm

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'


class UserLoginForm(forms.Form, BaseForm):
    username = forms.CharField(label='Username')

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
