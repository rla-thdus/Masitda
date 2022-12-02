from rest_framework import serializers

from orders.models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    cart = serializers.PrimaryKeyRelatedField(read_only=True, many=False)

    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, many=False)
    cart_items = CartItemSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        fields = '__all__'
