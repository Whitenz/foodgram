from rest_framework import serializers

from .models import AmountIngredient


def check_unique_ingredient(ingredients):
    list_ingredients = [ingredient.get('id') for ingredient in ingredients]
    if len(list_ingredients) != len(set(list_ingredients)):
        raise serializers.ValidationError(
            'Ингредиенты в рецепте не должны повторяться!'
        )


def add_ingredients_to_recipe(recipe, ingredients):
    for amount_ingredient in ingredients:
        ingredient = amount_ingredient.get('id')
        amount = amount_ingredient.get('amount')
        AmountIngredient.objects.get_or_create(
            recipe=recipe,
            ingredient=ingredient,
            amount=amount
        )
