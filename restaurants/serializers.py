from .models import Restaurant
from rest_framework import serializers


class RestaurantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, many=False)

    class Meta:
        model = Restaurant
        fields = '__all__'