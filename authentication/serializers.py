from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password','user_permissions', 'groups']
        
    
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'username', 'email', 'is_merchant']
        # exclude = ['user_permissions', 'groups']
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)