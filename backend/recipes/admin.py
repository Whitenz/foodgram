from django.contrib import admin

from .models import AmountIngredient, Ingredient, Recipe, Tag, TagRecipe


class AmountIngredientsInLine(admin.TabularInline):
    model = AmountIngredient
    raw_id_fields = ('ingredient',)
    extra = 0


class TagRecipeInline(admin.StackedInline):
    model = TagRecipe
    radio_fields = {'tag': admin.HORIZONTAL}
    extra = 0


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name',
                    'cooking_time', 'favorites_counter')
    search_fields = ('name',)
    list_filter = ('name', 'author', 'tags')
    inlines = (AmountIngredientsInLine, TagRecipeInline)


@admin.register(AmountIngredient)
class AmountIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    search_fields = ('recipe__name', 'ingredient__name')
    list_filter = ('recipe', 'ingredient')
