from djoser.views import UserViewSet

from rest_framework.permissions import AllowAny

from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    http_method_names = ('get', 'post')

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return (AllowAny(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'me'):
            return CustomUserSerializer
        return super().get_serializer_class()
