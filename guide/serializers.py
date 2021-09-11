from rest_framework import serializers
from .models import *


class GuideSerializer(serializers.ModelSerializer):

    class Meta:
        model = Guide
        fields = '__all__'


class GuideCategorySerializer(serializers.ModelSerializer):
    guides = GuideSerializer(many=True,required=False,read_only=True)
    class Meta:
        model = GuideCategory
        fields = '__all__'






