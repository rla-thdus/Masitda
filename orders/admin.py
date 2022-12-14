from django.contrib import admin

from orders.models import Cart, CartItem, OrderStatus, Order


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'ordered_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'menu', 'quantity', 'price']


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'user_id', 'total_price', 'order_status', 'date']

    def user_id(self, obj):
        return obj.cart.user.id
