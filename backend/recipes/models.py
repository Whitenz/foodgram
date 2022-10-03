from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from recipes.validators import HexValidator

User = get_user_model()


class Tag(models.Model):
    """
    Model for recipe tags.
    The model stores information about a name and color of the recipe tag in
     HEX-format, which is used to display the recipe label.
    """
    name = models.CharField(
        verbose_name=_('tag name'),
        max_length=200,
        db_index=True,
        unique=True,
    )
    color = models.CharField(
        verbose_name=_('tag colors'),
        max_length=7,
        unique=True,
        validators=(HexValidator(length=7),),
    )
    slug = models.SlugField(
        verbose_name=_('slug of the tag'),
        max_length=200,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Model for recipe ingredient.
    The model stores information about a name and measurement unit and is
     used to create a recipe.
    """
    name = models.CharField(
        verbose_name=_('ingredient name'),
        max_length=200,
        db_index=True,
    )
    measurement_unit = models.CharField(
        verbose_name=_('ingredient measurement measure'),
        max_length=200,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Model for recipe.
    The model stores information about an author, name, image, tags, cooking
     time, text description and ingredients for recipe. One recipe can have
     several tags and ingredients through M2M-field.
    """
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('recipe tags'),
        related_name='recipes',
        through='TagRecipe',
    )
    author = models.ForeignKey(
        User,
        verbose_name=_('author of the recipe'),
        related_name='recipes',
        on_delete=models.CASCADE,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name=_('recipe ingredients'),
        related_name='recipes',
        through='AmountIngredient'
    )
    name = models.CharField(
        verbose_name=_('recipe name'),
        max_length=200,
        db_index=True,
    )
    image = models.ImageField(
        verbose_name=_('recipe image'),
        upload_to='recipes/images/',
    )
    text = models.TextField(
        verbose_name=_('recipe description'),
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name=_('cooking time in minutes'),
        validators=(MinValueValidator(1),)
    )
    pub_date = models.DateTimeField(
        verbose_name=_('date of public'),
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date', 'name')
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')

    def __str__(self):
        return self.name

    @property
    def favorites_counter(self):
        """Return how many times a recipe has benn added to favorites."""
        return self.favorites.count()
    favorites_counter.fget.short_description = _('number in favorites')


class AmountIngredient(models.Model):
    """
    Model for amount ingredient in recipe.
    The model stores information about a recipe, ingredient and their amount.
    """
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_('recipe'),
        related_name='amount_ingredients',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name=_('ingredient'),
        related_name='amount_ingredients',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name=_('amount of ingredient for the recipe'),
        validators=(MinValueValidator(1),)
    )

    class Meta:
        verbose_name = _('amount of ingredients')
        verbose_name_plural = _('amount of ingredients')
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient'
            ),
        )

    def __str__(self):
        return (
            f'{self.recipe.name}: {self.ingredient.name} {self.amount}'
            f'{self.ingredient.measurement_unit}'
        )


class TagRecipe(models.Model):
    """An intermediate model for linking a tag and a recipe."""
    tag = models.ForeignKey(
        Tag,
        verbose_name=_('tag'),
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_('recipe'),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('tags of recipe')
        verbose_name_plural = _('tags of recipe')
        constraints = (
            models.UniqueConstraint(
                fields=('tag', 'recipe'),
                name='unique_tag_recipe'
            ),
        )


class Favorite(models.Model):
    """
    Model for favorite recipes.
    The model stores information about a user and him favorites recipe.
    """
    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
        related_name='favorites',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_('favorite recipes'),
        related_name='favorites',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('favorite')
        verbose_name_plural = _('favorite')
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_recipe'
            ),
        )


class Cart(models.Model):
    """
    Model for ingredients from recipes.
    The model stores information about a user and his favorite recipes.
    """
    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
        related_name='cart',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_('user shopping cart'),
        related_name='cart',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('shopping cart')
        verbose_name_plural = _('shopping cart')
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_cart_recipe'
            ),
        )
