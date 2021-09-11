from rest_framework import serializers
from .models import *


class PoiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poi
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class ResourceCategorySerializer(serializers.ModelSerializer):
    resourses = ResourceSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = ResourceCategory
        fields = '__all__'


class ResourceTypeSerializer(serializers.ModelSerializer):
    category = ResourceCategorySerializer(many=True, read_only=True, required=False)
    class Meta:
        model = ResourceType
        fields = '__all__'






