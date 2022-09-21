from django.contrib import admin

from recipes.models import Tag, Ingredient, Recipe


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name', 'text', 'cooking_time')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
