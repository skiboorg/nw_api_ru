from rest_framework import serializers
from .models import *
from user.models import User

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = '__all__'

class SkillTreeSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = SkillTree
        fields = '__all__'

class WeaponSerializer(serializers.ModelSerializer):
    trees = SkillTreeSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Weapon
        fields = '__all__'

class WeaponsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = [
            'id',
            'name',
            'name_slug',
            'image',
            'main_char',
            'is_selected'
        ]
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'nickname',
        ]

class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = BuildFeedback
        fields = '__all__'

class BuildSerializer(serializers.ModelSerializer):
    weapon1 = WeaponSerializer(many=False, required=False, read_only=True)
    weapon2 = WeaponSerializer(many=False, required=False, read_only=True)
    feedbacks = FeedbackSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Build
        fields = '__all__'

class BuildShortSerializer(serializers.ModelSerializer):
    weapon1 = WeaponsSerializer(many=False, required=False, read_only=True)
    weapon2 = WeaponsSerializer(many=False, required=False, read_only=True)
    created = serializers.CharField(source='get_humanize_time')
    class Meta:
        model = Build
        fields = '__all__'
