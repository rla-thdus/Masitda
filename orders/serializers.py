from rest_framework import serializers

from orders.models import Cart, CartItem, Order


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
    total_price = serializers.FloatField(read_only=True)

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        cart = Cart.objects.filter(id=order.cart.id)
        cart.update(ordered_at=order.date)
        return order

    class Meta:
        model = Order
        fields = 'cart, date, order_status, '
