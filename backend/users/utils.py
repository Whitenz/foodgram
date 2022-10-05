"""Module for additional methods used in the Users application."""

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Subscription


def add_subscribe_to_user(user_from, user_to, serializer):
    """Add subscription from current user to another."""
    if user_from == user_to:
        raise ValidationError(
            {'errors': _('You cannot subscribe to yourself.')}
        )

    subscription, created = Subscription.objects.get_or_create(
        user_from=user_from,
        user_to=user_to
    )
    if not created:
        raise ValidationError(
            {'errors': _('You have already subscribed to this user.')}
        )

    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


def del_subscribe_to_user(user_from, user_to):
    """Del subscription from current user to another."""
    try:
        subscription = Subscription.objects.get(user_from=user_from,
                                                user_to=user_to)
    except ObjectDoesNotExist:
        raise ValidationError(
            {'errors': _('You are not subscribed to this user.')}
        )

    subscription.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
