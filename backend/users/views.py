from djoser.views import UserViewSet

from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import CustomUserSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    http_method_names = ('get', 'post')
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return (AllowAny(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'me'):
            return CustomUserSerializer
        return super().get_serializer_class()

    @action(detail=False)
    def subscriptions(self, request):
        current_user = self.request.user
        subscriptions = current_user.following.all()
        serializer = self.get_serializer(subscriptions, many=True)
        return Response(serializer.data)
