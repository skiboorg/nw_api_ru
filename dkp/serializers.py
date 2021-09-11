from rest_framework import serializers
from .models import *
from user.models import User

class EventDkpSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDkp
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    players = EventDkpSerializer(many=True,required=False,read_only=True)
    class Meta:
        model = Event
        fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class EventDkpFullSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = EventDkp
        fields = '__all__'


class EventFullSerializer(serializers.ModelSerializer):

    players = EventDkpFullSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Event
        fields = '__all__'




