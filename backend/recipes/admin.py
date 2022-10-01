from django.contrib import admin

from .models import (AmountIngredient, Cart, Favorite, Ingredient, Recipe, Tag,
                     TagRecipe)


class AmountIngredientsInLine(admin.TabularInline):
    model = AmountIngredient
    raw_id_fields = ('ingredient',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name',
                    'cooking_time', 'favorites_counter')
    search_fields = ('name',)
    list_filter = ('name', 'author', 'tags')
    inlines = (AmountIngredientsInLine,)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user__username', 'recipe__name',)
    list_filter = ('user', 'recipe')


class CartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user__username', 'recipe__name',)
    list_filter = ('user', 'recipe')


class TagRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tag', 'recipe')
    search_fields = ('tag__name', 'recipe__name')
    list_filter = ('tag', 'recipe')


class AmountIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    search_fields = ('recipe__name', 'ingredient__name')
    list_filter = ('recipe', 'ingredient')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(TagRecipe, TagRecipeAdmin)
admin.site.register(AmountIngredient, AmountIngredientAdmin)
