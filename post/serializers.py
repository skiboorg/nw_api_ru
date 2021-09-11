from rest_framework import serializers
from .models import *


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostItem
        fields = [
            'id',
            'name',
            'name_slug',
            'image',
            'short_description',
            'views',
            'created_at'
        ]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostItem
        fields = '__all__'







