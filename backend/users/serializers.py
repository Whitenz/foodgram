from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Subscription

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
        read_only_fields = (settings.LOGIN_FIELD,)

    def get_is_subscribed(self, obj):
        return 'тут сделать инфу о подписке'  # DO IT !


class SubscriptionSerializer(serializers.ModelSerializer):
    user_from = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    user_to = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        model = Subscription
        fields = ('user_from', 'user_to',)
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user_from', 'user_to'),
                message='Подписка на этого автора уже оформлена.'
            )
        ]

    def validate(self, data):
        if self.context['request'].user == data['user_to']:
            raise serializers.ValidationError(
                'Нельзя оформить подписку на себя.'
            )
        return data
