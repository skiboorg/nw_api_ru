from rest_framework import serializers
from .models import *


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = '__all__'

class SocialItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialItem
        fields = '__all__'

class TextsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Texts
        fields = '__all__'







