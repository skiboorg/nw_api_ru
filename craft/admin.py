from django.contrib import admin
from .models import *


class RecipeItemInline (admin.TabularInline):
    model = RecipeItem
    extra = 0

class RecipeRecipeInline (admin.TabularInline):
    model = RecipeRecipe
    fk_name = 'recipe_item'
    extra = 0

class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [RecipeItemInline,RecipeRecipeInline]
    list_filter = ('category',)
    class Meta:
        model = Recipe


admin.site.register(Category)
admin.site.register(Recipe,RecipeAdmin)
admin.site.register(Item)
admin.site.register(RecipeRecipe)
admin.site.register(RecipeItem)