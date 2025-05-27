from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django_registration.forms import RegistrationForm


class UserRegisterForm(RegistrationForm):

    name = forms.CharField(max_length=30, required=True, label="Имя пользователя")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            User.USERNAME_FIELD,
            "name",
            "password1",
            "password2"
        ]