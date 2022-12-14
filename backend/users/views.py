from djoser.views import UserViewSet

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .paginators import CustomLimitPagination
from .serializers import CustomUserSerializer
from .utils import add_subscribe_to_user, del_subscribe_to_user
from recipes.serializers import RecipeSubscriptionSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """
    ViewSet for CustomUser model.
    Inherited from the User model of the djoser package. Add action methods
     for subscriptions to another user and then viewing their subscriptions.
    """
    serializer_class = CustomUserSerializer
    http_method_names = ('get', 'post', 'delete')
    pagination_class = CustomLimitPagination

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return (AllowAny(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'me'):
            return CustomUserSerializer
        return super().get_serializer_class()

    @action(detail=False,
            permission_classes=(IsAuthenticated,),
            serializer_class=RecipeSubscriptionSerializer)
    def subscriptions(self, request):
        current_user = self.get_instance()
        subscriptions = current_user.following.all()

        page = self.paginate_queryset(subscriptions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(subscriptions, many=True)
        return Response(serializer.data)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,),
            serializer_class=RecipeSubscriptionSerializer)
    def subscribe(self, request, id=None):
        user_from = self.get_instance()
        user_to = get_object_or_404(User, id=id)

        if request.method == 'POST':
            return add_subscribe_to_user(
                user_from=user_from,
                user_to=user_to,
                serializer=self.get_serializer(user_to)
            )

        return del_subscribe_to_user(
            user_from=user_from,
            user_to=user_to
        )
