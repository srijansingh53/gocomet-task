from django.contrib.auth.models import User
from django import forms

from .models import Tags

class UserForm(forms.ModelForm):

    password = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# class HandlerForm(forms.ModelForm):

#     class Meta:
#         model = Handlers
#         fields = ['handle', 'handler_name']
