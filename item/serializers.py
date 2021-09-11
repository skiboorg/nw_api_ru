from rest_framework import serializers
from .models import *



class ItemSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSubCategory
        fields = '__all__'


class ItemCategorySerializer(serializers.ModelSerializer):
    subcategories = ItemSubCategorySerializer(many=True, required=False, read_only=True)
    class Meta:
        model = ItemCategory
        fields = '__all__'



class PerkAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerkAttribute
        fields = '__all__'

class PerkSerializer(serializers.ModelSerializer):
    perk_attributes = PerkAttributeSerializer(many=True,required=False,read_only=True)
    class Meta:
        model = Perk
        fields = '__all__'

class PerkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerkType
        fields = '__all__'



class ItemAttributeScaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemAttributeScale
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    category = ItemCategorySerializer(many=False,required=False,read_only=True)
    subcategory= ItemSubCategorySerializer(many=False,required=False,read_only=True)
    perks = PerkSerializer(many=True,required=False,read_only=True)
    class Meta:
        model = Item
        fields = '__all__'





