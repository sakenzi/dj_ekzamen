from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username']

class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username')