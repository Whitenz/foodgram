from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class CustomUser(AbstractUser):
    """
    Custom user model.
    The model has the required attributes first_name, last_name, email. email
     must be unique.
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

    class Meta:
        verbose_name = _('user'),
        verbose_name_plural = _('users')
        ordering = ('username',)

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """
    A model for making subscriptions from one user to another.
    Used as an intermediate model: user_from - user who subscribed,
     user_to - who the subscription is for.
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
        return _('Subscription {} to {}').format(self.user_from, self.user_to)


class CustomTokenProxy(Token):
    class Meta:
        proxy = True
        verbose_name = _('token')
        verbose_name_plural = _('tokens')
        app_label = 'authtoken'
