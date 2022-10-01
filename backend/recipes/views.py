import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from .conf import cart_errors, favorite_errors
from .filters import IngredientFilter, RecipeFilter
from .models import AmountIngredient, Cart, Favorite, Ingredient, Recipe, Tag
from .paginators import CustomLimitPagination
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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
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
            serializer_class=ShortRecipeSerializer,
            pagination_class=CustomLimitPagination)
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

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = AmountIngredient.objects.filter(recipe__cart__user=user)
        shopping_list = ingredients.values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount')).order_by('ingredient__name')

        current_date = datetime.date.today().strftime('%d_%m_%Y')
        content = (f'Список покупок для {user.get_full_name()}'
                   f' от {current_date}\n')
        content += '\n'.join(
            (f"{_.get('ingredient__name')} - "
             f"{_.get('amount')} {_.get('ingredient__measurement_unit')}"
             ) for _ in shopping_list
        )
        filename = f'{user}_shopping_list_{current_date}.txt'

        response = HttpResponse(content, content_type='text.txt; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response
