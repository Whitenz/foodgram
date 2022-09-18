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
    following = models.ManyToManyField(
        'self',
        through='Subscription',
        related_name='followers',
        symmetrical=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """
    Модель для оформления подписок одного пользователя на другого.
    Используется в качестве промежуточной модели: user_from - пользователь
     оформивший подписку, user_to - на кого подписка.
    """
    user_from = models.ForeignKey(
        CustomUser,
        verbose_name=_('subscription from'),
        on_delete=models.CASCADE,
        related_name='subscription_from'
    )
    user_to = models.ForeignKey(
        CustomUser,
        verbose_name=_('subscribed to'),
        on_delete=models.CASCADE,
        related_name='subscribed_to'
    )

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')
        constraints = (
            models.UniqueConstraint(
                fields=['user_from', 'user_to'],
                name='unique_subscription'
            ),
        )

    def __str__(self) -> str:
        return f'Подписка {self.user_from} на {self.user_to}'
