from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny


class CustomUserViewSet(UserViewSet):
    http_method_names = ('get', 'post')

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return (AllowAny(),)
        return super().get_permissions()
