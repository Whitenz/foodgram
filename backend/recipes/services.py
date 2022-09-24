from .models import AmountIngredient


def add_ingredients_to_recipe(recipe, ingredients):
    for ingredient_set in ingredients:
        ingredient = ingredient_set.get('id')
        amount = ingredient_set.get('amount')
        AmountIngredient.objects.get_or_create(
            recipe=recipe,
            ingredient=ingredient,
            amount=amount
        )
