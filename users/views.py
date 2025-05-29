from typing import Any

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from django_registration.backends.activation.views import RegistrationView, ActivationView

from .forms import UserRegisterForm

class CustomRegistrationView(RegistrationView):
    form_class = UserRegisterForm
    success_url = "/"
    template_name = "django_registration/registration_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add honeypot field to context."""
        context = super().get_context_data(**kwargs)

        return context

    def form_valid(self, form):
        check_email_message = """Спасибо за регистрацию. Для продолжения смотрите сообщение отправленное на Вашу почту"""
        messages.info(self.request, check_email_message)

        return super().form_valid(form)

@login_required # Require user logged in before they can access profile page
def profile(request):
    return render(request, 'users/profile.html')
