from djoser.views import UserViewSet

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .conf import subscription_errors
from .models import Subscription
from .serializers import CustomUserSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    http_method_names = ('get', 'post', 'delete')

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return (permissions.AllowAny(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'me'):
            return CustomUserSerializer
        return super().get_serializer_class()

    @action(detail=False)
    def subscriptions(self, request):
        current_user = self.get_instance()
        subscriptions = current_user.following.all()
        serializer = self.get_serializer(subscriptions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, id=None):
        user_from = self.get_instance()
        user_to = get_object_or_404(User, id=id)

        if request.method == 'POST':
            if user_from == user_to:
                return Response(
                    data=subscription_errors.get('add_to_yourself'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            subscription, created = Subscription.objects.get_or_create(
                user_from=user_from,
                user_to=user_to
            )
            if created:
                serializer = self.get_serializer(user_to)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                data=subscription_errors.get('already_exists'),
                status=status.HTTP_400_BAD_REQUEST
            )

        subscription = Subscription.objects.filter(
            user_from=user_from,
            user_to=user_to
        ).first()
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            data=subscription_errors.get('not_signed'),
            status=status.HTTP_400_BAD_REQUEST
        )
