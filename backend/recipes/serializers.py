import base64

from djoser.conf import settings

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import AmountIngredient, Ingredient, Recipe, Tag
from .utils import check_unique_ingredient, set_ingredients_to_recipe
from users.serializers import CustomUserSerializer

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """
    Serializer for recipe image field.
    Get image from request in base64 encoding and then saves to image file.
    """
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            user = self.context['request'].user
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),
                               name=f'{user}_recipe.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient model."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AmountIngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for AmountIngredient model.
    Get ingredient id and its amount with POST request for create recipe.
    For GET request return ingredient id, name, amount and measurement unit.
    """
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = AmountIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = instance.ingredient.id
        return data


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for Recipe model.
    In POST request get ingredient tags, ingredients with amount, name, text
    description, cooking time and image for create new recipe. Ingredients in
    should be unique. For GET request add fields author of the recipe,
    is_favorited and is_in_shopping_cart.
    """
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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tags'] = TagSerializer(instance.tags.all(), many=True).data
        return data

    def validate_ingredients(self, value):
        check_unique_ingredient(value)
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('amount_ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        set_ingredients_to_recipe(recipe, ingredients)
        return recipe

    def update(self, recipe, validated_data):
        tags = validated_data.pop('tags', recipe.tags)
        ingredients = validated_data.pop(
            'amount_ingredients', recipe.amount_ingredients
        )
        for attr, value in validated_data.items():
            setattr(recipe, attr, value)
        recipe.tags.set(tags)
        recipe.ingredients.clear()
        set_ingredients_to_recipe(recipe, ingredients)
        recipe.save()
        return recipe

    def get_is_favorited(self, recipe):
        current_user = self.context['request'].user
        return current_user.is_authenticated and (
            current_user.favorites.filter(recipe=recipe).exists()
        )

    def get_is_in_shopping_cart(self, recipe):
        current_user = self.context['request'].user
        return current_user.is_authenticated and (
            current_user.cart.filter(recipe=recipe).exists()
        )


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Serializer for short view info about recipe."""
    class Meta:
        model = Recipe
        fields = 'id', 'name', 'image', 'cooking_time'


class RecipeSubscriptionSerializer(CustomUserSerializer):
    """
    Serializer for view subscriptions of the current user.
    Method get_recipes allows limit recipes for views by query parameter
     recipes_limit, get_recipes_count returns  the number of author's recipes.
    """
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, user):
        recipes = user.recipes.all()
        limit = self.context['request'].query_params.get('recipes_limit')
        if limit is not None and limit.isdigit():
            recipes = recipes[:int(limit)]
        return ShortRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, user):
        return user.recipes.count()
