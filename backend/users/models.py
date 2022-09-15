from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя.
    Модель имеет обязательные атрибуты first_name, last_name, email. email
    должен быть уникальным.
    """

    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'), unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
