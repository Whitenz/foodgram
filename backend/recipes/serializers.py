import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from users.serializers import CustomUserSerializer
from recipes.models import Ingredient, Recipe, Tag, AmountIngredient
from .services import add_ingredients_to_recipe, check_unique_ingredient


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AmountIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = AmountIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    ingredients = AmountIngredientSerializer(
        source='amount_ingredients',
        many=True,
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def validate_ingredients(self, value):
        check_unique_ingredient(value)
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('amount_ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        add_ingredients_to_recipe(recipe, ingredients)
        return recipe

    def update(self, recipe, validated_data):
        recipe.cooking_time = validated_data.get(
            'cooking_time', recipe.cooking_time
        )
        recipe.name = validated_data.get('name', recipe.name)
        recipe.image = validated_data.get('image', recipe.image)
        recipe.text = validated_data.get('text', recipe.text)

        tags = validated_data.get('tags', recipe.tags)
        ingredients = validated_data.get(
            'amount_ingredients', recipe.amount_ingredients
        )
        recipe.tags.set(tags)
        recipe.ingredients.clear()
        add_ingredients_to_recipe(recipe, ingredients)

        recipe.save()
        return recipe

    def get_is_favorited(self, obj):
        return 'проверка на избранное'

    def get_is_in_shopping_cart(self, obj):
        return 'проверка на наличие в корзине'
