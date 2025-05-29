from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class UserManager(BaseUserManager):
    """Custom user model manager where email is the unique identifiers for
    authentication instead of usernames.

    Source: https://testdriven.io/blog/django-custom-user-model/
    """

    def create_user(
        self,
        email: str,
        password: str,
        **extra_fields: dict[str, str | bool],
    ) -> "User":
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("Введите почту")
        email = self.normalize_email(email)
        user: User = self.model(email=email, **extra_fields)  # type: ignore
        user.set_password(password)
        user.save()

        return user


class User(AbstractUser):
    # email must be unique since it is used as the username field
    email = models.EmailField(unique=True, verbose_name="Почта")
    # disable username field
    name = None
    username = models.CharField(
        ("username"),
        max_length=150,
        unique=False,
        validators=[AbstractUser.username_validator],
    )
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    REQUIRED_FIELDS = []