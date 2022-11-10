from .models import Restaurant
from rest_framework import serializers


class RestaurantSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.id

    class Meta:
        model = Restaurant
        fields = '__all__'