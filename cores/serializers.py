from .models import Restaurant, Menu, CartItem, Cart, Order
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


class OrderSerializer(serializers.ModelSerializer):
    cart = serializers.PrimaryKeyRelatedField(read_only=True, many=False)
    total_price = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        cart = Cart.objects.filter(id=order.cart.id)
        cart.update(ordered_at=order.date)
        return order

    class Meta:
        model = Order
        fields = '__all__'
