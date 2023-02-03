from .models import Restaurant, Menu, CartItem, Cart, Order, Review
from rest_framework import serializers


class MenuSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(read_only=True, many=False)

    class Meta:
        model = Menu
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, many=False)
    menu_set = MenuSerializer(many=True, read_only=True)
    rating_avg = serializers.FloatField(read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    cart = serializers.PrimaryKeyRelatedField(read_only=True, many=False)

    def create(self, validated_data):
        cart_item = CartItem.objects.create(**validated_data)
        cart = Cart.objects.filter(id=cart_item.cart.id)
        cart.update(restaurant=cart_item.menu.restaurant)
        return cart_item

    class Meta:
        model = CartItem
        fields = '__all__'


class CartItemDetailSerializer(serializers.ModelSerializer):
    cart = serializers.PrimaryKeyRelatedField(read_only=True, many=False)
    menu = MenuSerializer(read_only=True, many=False)

    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, many=False)
    cart_items = CartItemDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True, many=False)
    total_price = serializers.IntegerField(read_only=True)
    delivery_price = serializers.IntegerField(read_only=True)
    amount_payment = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        cart = Cart.objects.filter(id=order.cart.id)
        cart.update(ordered_at=order.date)
        return order

    class Meta:
        model = Order
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True, many=False)

    class Meta:
        model = Review
        fields = '__all__'
