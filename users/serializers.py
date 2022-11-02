from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    class Meta:
        model = User
        fields = ['nickname', 'email', 'address', 'phone', 'password']
