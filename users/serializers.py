from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            nickname = validated_data['nickname'],
            address = validated_data['address'],
            password = validated_data['password']
        )
        return user
    class Meta:
        model = User
        fields = ['nickname', 'email', 'address', 'password']
