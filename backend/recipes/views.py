from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from .conf import cart_errors, favorite_errors
from .models import Cart, Favorite, Ingredient, Recipe, Tag
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          ShortRecipeSerializer, TagSerializer)
from .services import add_recipe_to_linked_model, del_recipe_from_linked_model


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,),
            serializer_class=ShortRecipeSerializer)
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return add_recipe_to_linked_model(
                recipe=self.get_object(),
                user=self.request.user,
                linked_model=Favorite,
                serializer=self.get_serializer(self.get_object()),
                errors=favorite_errors
            )
        return del_recipe_from_linked_model(
            recipe=self.get_object(),
            user=self.request.user,
            linked_model=Favorite,
            errors=favorite_errors
        )

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,),
            serializer_class=ShortRecipeSerializer)
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return add_recipe_to_linked_model(
                recipe=self.get_object(),
                user=self.request.user,
                linked_model=Cart,
                serializer=self.get_serializer(self.get_object()),
                errors=cart_errors
            )
        return del_recipe_from_linked_model(
            recipe=self.get_object(),
            user=self.request.user,
            linked_model=Cart,
            errors=cart_errors
        )
