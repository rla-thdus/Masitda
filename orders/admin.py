from django.contrib import admin

from orders.models import Cart, CartItem, OrderStatus, Order


@admin.register(Cart)
class BlanketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']


@admin.register(CartItem)
class BlanketItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'menu', 'quantity']


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'user', 'total_price', 'order_status', 'date']
