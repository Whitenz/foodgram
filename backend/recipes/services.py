from rest_framework import serializers, status
from rest_framework.response import Response

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


def add_recipe_to_linked_model(recipe, linked_model, user, serializer, errors):
    obj, created = linked_model.objects.get_or_create(user=user,
                                                      recipe=recipe)
    if created:
        return Response(data=serializer.data,
                        status=status.HTTP_201_CREATED)

    return Response(data=errors.get('already_exists'),
                    status=status.HTTP_400_BAD_REQUEST)


def del_recipe_from_linked_model(recipe, linked_model, user, errors):
    obj = linked_model.objects.filter(user=user, recipe=recipe).first()
    if obj:
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(data=errors.get('not_exist'),
                    status=status.HTTP_400_BAD_REQUEST)
