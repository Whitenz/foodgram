from djoser.conf import settings
from djoser.serializers import UserSerializer

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        current_user = self.context['request'].user
        if current_user.is_anonymous or current_user == obj:
            return False
        return current_user.following.filter(pk=obj.pk).exists()
