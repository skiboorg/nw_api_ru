from rest_framework import serializers
from .models import *
from user.models import User

class GuildsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guild
        fields = [
            'id',
            'name',
            'name_slug',
            'image',
            'fraction',
            'size',
            'total_rating',
            'server',
            'style',
            'feedbacks',
        ]


class GuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guild
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'nickname',
        ]

class GuildFeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = GuildFeedback
        fields = '__all__'




