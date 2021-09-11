from rest_framework import serializers
from .models import *




class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class RecipeItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = RecipeItem
        fields = '__all__'


class Recipe0Serializer(serializers.ModelSerializer):
    items = RecipeItemSerializer(many=True,required=False,read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

class RecipeRecipeSerializer(serializers.ModelSerializer):
    main_recipe = Recipe0Serializer(many=False, required=False, read_only=True)
    class Meta:
        model = RecipeRecipe
        fields = '__all__'

class RecipeSerializer(serializers.ModelSerializer):
    items = RecipeItemSerializer(many=True,required=False,read_only=True)
    recipe_items = RecipeRecipeSerializer(many=True,required=False,read_only=True)
    class Meta:
        model = Recipe
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(many=True,required=False,read_only=True)
    class Meta:
        model = Category
        fields = '__all__'



