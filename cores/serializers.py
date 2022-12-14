from .models import Restaurant, Menu
from rest_framework import serializers


class MenuSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(read_only=True, many=False)

    class Meta:
        model = Menu
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, many=False)
    menu_set = MenuSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'
