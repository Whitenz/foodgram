from djoser.conf import settings
from djoser.serializers import UserSerializer

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """
    Serializer for User model.
    Add method for check subscription to another user.
    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'is_subscribed',
        )

    def get_is_subscribed(self, user_to):
        user_from = self.context['request'].user
        return user_from.is_authenticated and user_from != user_to and (
            user_from.following.filter(pk=user_to.pk).exists()
        )
