import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import AmountIngredient


def check_unique_ingredient(ingredients):
    list_ingredients = [ingredient.get('id') for ingredient in ingredients]
    if len(list_ingredients) != len(set(list_ingredients)):
        raise serializers.ValidationError(
            {'errors': _('Ingredients should not be repeated.')}
        )


def add_ingredients_to_recipe(recipe, ingredients):
    objs = []
    for ingredient in ingredients:
        objs.append(AmountIngredient(recipe=recipe,
                                     ingredient=ingredient.get('id'),
                                     amount=ingredient.get('amount')))
    AmountIngredient.objects.bulk_create(objs)


def add_recipe_to_linked_model(recipe, linked_model, user, serializer):
    obj, created = linked_model.objects.get_or_create(user=user,
                                                      recipe=recipe)
    if not created:
        raise ValidationError(
            {'errors': _('You have already added this recipe.')}
        )

    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


def del_recipe_from_linked_model(recipe, linked_model, user):
    try:
        obj = linked_model.objects.get(user=user, recipe=recipe)
    except ObjectDoesNotExist:
        raise ValidationError(
            {'errors': _('You did not add this recipe.')}
        )
    obj.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


def get_data_for_shopping_list(user):
    ingredients = AmountIngredient.objects.filter(recipe__cart__user=user)
    shopping_list = ingredients.values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(amount=Sum('amount')).order_by('ingredient__name')

    today = datetime.date.today().strftime('%d_%m_%Y')
    content = (
        _('Shopping list for {} - {}\n\n').format(user.get_full_name(), today)
    )
    content += '\n'.join(
        (f'{obj.get("ingredient__name")} - '
         f'{obj.get("amount")} {obj.get("ingredient__measurement_unit")}'
         ) for obj in shopping_list
    )
    filename = f'{user}_shopping_list_{today}.txt'
    response = HttpResponse(content,
                            content_type='text.txt; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename={filename}'

    return response
