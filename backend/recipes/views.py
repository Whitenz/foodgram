from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from .filters import IngredientFilter, RecipeFilter
from .models import Cart, Favorite, Ingredient, Recipe, Tag
from .paginators import CustomLimitPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          ShortRecipeSerializer, TagSerializer)
from .utils import (add_recipe_to_linked_model, del_recipe_from_linked_model,
                    get_data_for_shopping_list)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for model Tag.
    Read only mode.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for model Ingredient.
    Read only mode. Allow filters ingredient by name.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for model Recipe.
    Supports methods GET, POST, PATCH, DELETE. Allow filters recipe by tags,
     field is_favorited and is_in_shopping_cart. Add action methods for add/del
     recipe to favorite list and shopping cart. Add action method for download
     shopping list for current user.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    pagination_class = CustomLimitPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,),
            serializer_class=ShortRecipeSerializer)
    def favorite(self, request, pk=None):
        """Action method for add/del recipe to favorite for current user."""
        if request.method == 'POST':
            return add_recipe_to_linked_model(
                recipe=self.get_object(),
                user=request.user,
                linked_model=Favorite,
                serializer=self.get_serializer(self.get_object()),
            )
        return del_recipe_from_linked_model(
            recipe=self.get_object(),
            user=request.user,
            linked_model=Favorite,
        )

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,),
            serializer_class=ShortRecipeSerializer)
    def shopping_cart(self, request, pk=None):
        """
        Action method for add/del recipe to shopping cart for
         current user.
        """
        if request.method == 'POST':
            return add_recipe_to_linked_model(
                recipe=self.get_object(),
                user=request.user,
                linked_model=Cart,
                serializer=self.get_serializer(self.get_object()),
            )
        return del_recipe_from_linked_model(
            recipe=self.get_object(),
            user=request.user,
            linked_model=Cart,
        )

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        """Method for download shopping list in a txt file."""
        return get_data_for_shopping_list(user=request.user)
