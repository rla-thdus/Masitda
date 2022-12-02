from rest_framework import serializers

from orders.models import Cart, BlanketItem


class BlanketItemSerializer(serializers.ModelSerializer):
    blanket = serializers.PrimaryKeyRelatedField(read_only=True, many=False)

    class Meta:
        model = BlanketItem
        fields = '__all__'

class BlanketSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, many=False)
    blanket_items = BlanketItemSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        fields = '__all__'
