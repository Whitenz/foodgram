from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
        unique=True
    )
    color = models.CharField(
        max_length=7,
        unique=True
    )
    slug = models.SlugField(
        max_length=200,
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self) -> str:
        return self.slug


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True
    )
    measurement_unit = models.CharField(
        max_length=200
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        through='TagRecipe',
    )
    author = models.ForeignKey(
        User,
        verbose_name=_('author of the recipe'),
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='AmountIngredient'
    )
    name = models.CharField(
        verbose_name=_('recipe name'),
        max_length=200,
        db_index=True,
    )
    image = models.ImageField(
        verbose_name=_('recipe image'),
        upload_to='recipes/images/'
    )
    text = models.TextField(
        verbose_name=_('text description of the recipe')
    )
    cooking_time = models.IntegerField(
        verbose_name=_('cooking time in minutes')
    )
    pub_date = models.DateTimeField(
        verbose_name=_('date of public'),
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date', 'name')
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')

    def __str__(self) -> str:
        return self.name


class AmountIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        # related_name='ingredients',
        verbose_name=_('recipe'),
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        # related_name='amounts',
        verbose_name=_('ingredient'),
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        verbose_name=_('amount of ingredient for the recipe'),
        default=1
    )


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
