from django_filters import rest_framework as filter

from .models import Ingredient, Recipe


class IngredientFilter(filter.FilterSet):
    name = filter.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filter.FilterSet):
    tags = filter.CharFilter(field_name='tags__slug')
    is_favorited = filter.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filter.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(cart__user=self.request.user)
        return queryset
